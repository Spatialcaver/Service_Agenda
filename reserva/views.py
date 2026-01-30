from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, date
from django.db.models import Sum, Count
from estabelecimento.models import Servicos, Estabelecimento
from user.models import Funcionario
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
            
            inicio_dt = datetime.combine(data_agendamento, hora_inicio)
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
                    r_fim = (datetime.combine(r.data, r.hora) + r.servico.duracao).time()

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


class DashboardEstabelecimentoView(APIView):
    def get(self, request):
        est_id = request.query_params.get('estabelecimento_id')
        data_query_str = request.query_params.get('data', date.today().isoformat())
        
        if not est_id:
            return Response({"erro": "ID do estabelecimento é obrigatório"}, status=400)

        # Converte a data da query para objeto date para cálculos
        data_query = date.fromisoformat(data_query_str)

        # --- PARTE B: Filtros de Reservas e Status ---
        reservas_hoje = Reserva.objects.filter(
            estabelecimento_id=est_id,
            data=data_query
        ).select_related('funcionario', 'servico', 'usuario')

        # Métricas focadas em Status (B)
        total_agendamentos = reservas_hoje.count()
        concluidos = reservas_hoje.filter(status='C').count()
        cancelados = reservas_hoje.filter(status='X').count()
        
        # Faturamento apenas do que foi concluído vs o que está previsto (Pendente)
        faturamento_realizado = reservas_hoje.filter(status='C').aggregate(Sum('servico__preco'))['servico__preco__sum'] or 0
        faturamento_previsto = reservas_hoje.filter(status='P').aggregate(Sum('servico__preco'))['servico__preco__sum'] or 0

        # --- PARTE A: Desempenho dos Últimos 7 Dias (Gráficos) ---
        sete_dias_atras = data_query - timedelta(days=7)
        desempenho_semana = Reserva.objects.filter(
            estabelecimento_id=est_id,
            data__range=[sete_dias_atras, data_query],
            status='C' # Contamos faturamento apenas de serviços finalizados
        ).values('data').annotate(
            total_faturado=Sum('servico__preco'),
            qtd_servicos=Count('id')
        ).order_by('data')

        # 2. Agenda Detalhada
        agenda_detalhada = ReservaSerializer(reservas_hoje.order_by('hora'), many=True).data

        return Response({
            "metrics": {
                "hoje": {
                    "total": total_agendamentos,
                    "concluidos": concluidos,
                    "cancelados": cancelados,
                    "faturamento_realizado": faturamento_realizado,
                    "faturamento_pendente": faturamento_previsto,
                }
            },
            "chart_data": desempenho_semana,
            "agenda": agenda_detalhada
        })