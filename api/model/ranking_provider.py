from db import *

class RankingProvider(object):

    def __init__(self, id_ranking_provider=None, db_row=None):
        if db_row != None:
            self.fill_from_data_row(db_row)
        elif id_ranking_provider != None:
            rows, _ = self.db_select(id_ranking_provider=id_ranking_provider)
            if len(rows) == 0:
                raise KeyError("row not found")
            self.fill_from_data_row(rows[0])

    def fill_from_data_row(self, row):
        self.id_ranking_provider = row["id_ranking_provider"]
        self.name = row["name"]
        self.date_changed = row["date_changed"]

    def insert(self):
        self.id_ranking_provider = pg_execute("\
        insert into ranking_provider(\
            name,\
            date_changed)\
        values(%s,%s) returning id_ranking_provider",
        (
            self.name,
            self.date_changed
        ))

    def update(self):
        pg_execute("\
        update\
            ranking_provider\
        set\
            name = %s,\
            date_changed = %s\
        where\
            id_ranking_provider = %s",
        (
            self.name,
            self.date_changed,
            self.id_ranking_provider
        ))

    def delete(self):
        pg_execute("\
        delete from\
            ranking_provider\
        where\
            id_ranking_provider = %s",
        (
            self.id_ranking_provider,
        ))

    def reload(self):
        rows, _ = self.db_select(id_ranking_provider=self.id_ranking_provider)
        self.fill_from_data_row(rows[0])                   

    @staticmethod
    def db_select(id_ranking_provider=None,
                  sort_by=None,
                  results_page=None,
                  results_page_size=None,
                  filter_by=None):
        order_string = ""
        if sort_by:
            sort_by_sanitized=sanitize(sort_by)
            order_string=" order by {0}".format(sort_by_sanitized)

        limit_string=""
        if results_page and results_page_size:
            start_record=(results_page - 1) * results_page_size
            limit_string=" offset {0} limit {1}".format(
                int(start_record), int(results_page_size))

        filter_string = ""
        if filter_by and len(filter_by) > 0:
            for f in filter_by:
                filter_string += " and {0} ilike '{1}%%'".format(sanitize(f["id"]), sanitize(f["value"]))

        return pg_select_rows_with_count("\
            select\
            count(*) over() as row_count,\
                id_ranking_provider,\
                name,\
                date_changed\
            from\
                ranking_provider\
            where\
                (%(id_ranking_provider)s is null or id_ranking_provider = %(id_ranking_provider)s)\
           {0} {1} {2}".format(filter_string, order_string, limit_string),
            {
                "id_ranking_provider": id_ranking_provider
            })

    @staticmethod
    def get_all():
        items = []
        rows, _ = RankingProvider.db_select()
        for row in rows:
            item = RankingProvider()
            item.fill_from_data_row(row)
            items.append(item)
        
        return items

    @staticmethod
    def get_paged(id_ranking_provider=None,
                  sort_by=None,
                  results_page=None,
                  results_page_size=None,
                  filter_by=None):
                  
        items = []

        rows, row_count = RankingProvider.db_select(
            id_ranking_provider=id_ranking_provider,
            sort_by=sort_by,
            results_page=results_page,
            results_page_size=results_page_size,
            filter_by=filter_by)

        for row in rows:
            item = RankingProvider()
            item.fill_from_data_row(row)
            items.append(item)

        return items, row_count
