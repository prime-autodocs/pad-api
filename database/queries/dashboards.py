from collections import defaultdict
from datetime import datetime

from sqlalchemy import func

from database.database import db
from database.models.customers import Customers
from database.models.vehicles import Vehicles


class DashboardsQueries:
    @classmethod
    def get_total_customers(cls) -> int:
        """
        Retorna o total de clientes cadastrados.
        """
        return db.query(func.count(Customers.id)).scalar() or 0

    @classmethod
    def get_total_vehicles(cls) -> int:
        """
        Retorna o total de veículos cadastrados.
        """
        return db.query(func.count(Vehicles.id)).scalar() or 0

    @classmethod
    def get_new_customers_current_month(cls) -> int:
        """
        Retorna quantos clientes foram cadastrados no mês corrente
        (com base na coluna created_at).
        """
        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        if month_start.month == 12:
            next_month_start = month_start.replace(year=month_start.year + 1, month=1)
        else:
            next_month_start = month_start.replace(month=month_start.month + 1)

        return (
            db.query(func.count(Customers.id))
            .filter(Customers.created_at >= month_start)
            .filter(Customers.created_at < next_month_start)
            .scalar()
            or 0
        )

    @classmethod
    def get_services_current_month(cls) -> int:
        """
        Retorna quantos serviços foram realizados no mês corrente
        (com base na coluna created_at).
        """
        # TODO: Implementar a consulta real para os serviços realizados no mês corrente
        return 0

    # --------- Séries temporais de novos clientes ---------

    @classmethod
    def get_new_customers_grouped_by_month_last_12(cls):
        """
        Retorna uma lista com a quantidade de novos clientes por mês
        nos últimos 12 meses.

        Cada item do retorno é um dict: {"year": int, "month": int, "count": int}
        """
        now = datetime.utcnow()
        year = now.year
        month = now.month

        # Gera a lista de (ano, mês) dos últimos 12 meses (do mais antigo para o mais recente)
        months = []
        for i in range(11, -1, -1):
            y = year
            m = month - i
            while m <= 0:
                y -= 1
                m += 12
            months.append((y, m))

        start_year, start_month = months[0]
        start_date = datetime(start_year, start_month, 1)

        last_year, last_month = months[-1]
        if last_month == 12:
            end_date = datetime(last_year + 1, 1, 1)
        else:
            end_date = datetime(last_year, last_month + 1, 1)

        rows = (
            db.query(Customers.created_at)
            .filter(Customers.created_at >= start_date)
            .filter(Customers.created_at < end_date)
            .all()
        )

        counts = {(y, m): 0 for (y, m) in months}
        for (created_at,) in rows:
            if created_at is None:
                continue
            key = (created_at.year, created_at.month)
            if key in counts:
                counts[key] += 1

        result = []
        for (y, m) in months:
            result.append({"year": y, "month": m, "count": counts[(y, m)]})
        return result

    @classmethod
    def get_new_customers_grouped_by_year(cls):
        """
        Retorna uma lista com a quantidade de novos clientes por ano.

        Cada item do retorno é um dict: {"year": int, "count": int}
        """
        rows = db.query(Customers.created_at).all()

        counts = defaultdict(int)
        for (created_at,) in rows:
            if created_at is None:
                continue
            counts[created_at.year] += 1

        result = []
        for year in sorted(counts.keys()):
            result.append({"year": year, "count": counts[year]})
        return result
