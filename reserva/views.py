from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, combine, timedelta
from estabelecimento.models import Funcionario, Servicos
from .models import Reserva
from .serializers import ReservaSerializer

class ReservaView(APIView):

    def post(self, request):


        serializer = ReservaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        reservas = Reserva.objects.all()
        serializer = ReservaSerializer(reservas, many=True)
        return Response(serializer.data)

    
    def put(self, request, pk):
        reserva = Reserva.objects.get(pk=pk)
        serializer = ReservaSerializer(reserva, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reserva = Reserva.objects.get(pk=pk)
        reserva.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DisponibilidadeView(APIView):
   def get(self, request):
        # Parâmetros esperados do Front-end
        data_param = request.query_params.get('data')
        hora_param = request.query_params.get('hora')
        servico_id = request.query_params.get('servico_id')
        est_id = request.query_params.get('estabelecimento_id')

        if not all([data_param, hora_param, servico_id, est_id]):
            return Response({"erro": "Parâmetros insuficientes"}, status=400)

        try:
            # 1. Preparação dos dados
            data_agendamento = datetime.strptime(data_param, '%Y-%m-%d').date()
            hora_inicio = datetime.strptime(hora_param, '%H:%M').time()
            servico = Servicos.objects.get(id=servico_id)
            estabelecimento = Estabelecimento.objects.get(id=est_id)
            
            inicio_dt = combine(data_agendamento, hora_inicio)
            fim_dt = inicio_dt + servico.duracao
            hora_fim = fim_dt.time()

            # 2. Validação: O estabelecimento está aberto neste horário?
            # Verifica se o horário pretendido está fora do expediente
            if hora_inicio < estabelecimento.horario_abertura or hora_fim > estabelecimento.horario_fechamento:
                return Response({
                    "disponivel": False,
                    "mensagem": "Horário fora do período de funcionamento do estabelecimento.",
                    "funcionarios": []
                }, status=status.HTTP_200_OK)

            # 3. Verificação por Funcionário
            funcionarios = Funcionario.objects.filter(estabelecimento=estabelecimento)
            resultado_funcionarios = []
            
            for func in funcionarios:
                # Busca reservas do dia para este funcionário
                reservas_dia = Reserva.objects.filter(
                    funcionario=func,
                    data=data_agendamento
                )

                ocupado = False
                for r in reservas_dia:
                    # Cálculo do intervalo da reserva existente
                    r_inicio = r.hora
                    r_fim = (combine(r.data, r.hora) + r.servico.duracao).time()

                    # Lógica de Sobreposição: (Início1 < Fim2) e (Fim1 > Início2)
                    if hora_inicio < r_fim and hora_fim > r_inicio:
                        ocupado = True
                        break
                
                resultado_funcionarios.append({
                    "id": str(func.id),
                    "nome": func.nome,
                    "disponivel": not ocupado,
                    "motivo": "Ocupado" if ocupado else "Livre"
                })

            # 4. Resposta Consolidada
            # Se nenhum funcionário estiver livre, o horário como um todo está indisponível
            algum_disponivel = any(f['disponivel'] for f in resultado_funcionarios)

            return Response({
                "horario_valido": True,
                "algum_funcionario_disponivel": algum_disponivel,
                "funcionarios": resultado_funcionarios
            }, status=status.HTTP_200_OK)

        except (Servicos.DoesNotExist, Estabelecimento.DoesNotExist):
            return Response({"erro": "Serviço ou Estabelecimento não encontrado"}, status=404)
        except Exception as e:
            return Response({"erro": str(e)}, status=500)