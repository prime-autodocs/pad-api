from interfaces.api.schemas.dashboards import (
    DashboardSummary,
    DashboardPeriod,
    NewCustomersTimeSeries,
    NewCustomersPoint,
)
from database.queries.dashboards import DashboardsQueries


class Dashboard:
    @classmethod
    def get_summary(cls) -> DashboardSummary:
        """
        Retorna os números principais para o dashboard:
        - total de clientes
        - total de veículos
        - novos clientes no mês corrente
        - serviços realizados no mês corrente
        """
        total_customers = DashboardsQueries.get_total_customers()
        total_vehicles = DashboardsQueries.get_total_vehicles()
        new_customers_month = DashboardsQueries.get_new_customers_current_month()
        services_month = DashboardsQueries.get_services_current_month()
        
        return DashboardSummary(
            total_customers=total_customers,
            total_vehicles=total_vehicles,
            new_customers_current_month=new_customers_month,
            services_current_month=services_month,
        )

    @classmethod
    def get_new_customers_timeseries(cls, period: DashboardPeriod) -> NewCustomersTimeSeries:
        """
        Retorna a série temporal de novos clientes de acordo com o período:
        - monthly: últimos 12 meses (1 barra por mês)
        - quarter: últimos 4 trimestres (agrupando os 12 meses em 4 blocos de 3)
        - annual: todos os anos disponíveis
        """
        # Labels para os meses (em PT-BR abreviado)
        month_labels = [
            "Jan",
            "Fev",
            "Mar",
            "Abr",
            "Mai",
            "Jun",
            "Jul",
            "Ago",
            "Set",
            "Out",
            "Nov",
            "Dez",
        ]

        if period == DashboardPeriod.monthly:
            monthly_data = DashboardsQueries.get_new_customers_grouped_by_month_last_12()
            points = [
                NewCustomersPoint(
                    label=month_labels[item["month"] - 1],
                    value=item["count"],
                )
                for item in monthly_data
            ]

        elif period == DashboardPeriod.quarter:
            # Usamos os mesmos 12 meses, agrupando de 3 em 3
            monthly_data = DashboardsQueries.get_new_customers_grouped_by_month_last_12()
            points = []
            for i in range(0, 12, 3):
                group = monthly_data[i : i + 3]
                total = sum(item["count"] for item in group)
                quarter_index = len(points) + 1
                label = f"{quarter_index}º Tri"
                points.append(NewCustomersPoint(label=label, value=total))

        elif period == DashboardPeriod.annual:
            yearly_data = DashboardsQueries.get_new_customers_grouped_by_year()
            points = [
                NewCustomersPoint(
                    label=str(item["year"]),
                    value=item["count"],
                )
                for item in yearly_data
            ]
        else:
            # fallback defensivo; FastAPI deve validar o Enum antes
            points = []

        return NewCustomersTimeSeries(period=period, points=points)
