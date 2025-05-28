import psycopg2
from typing import List, Dict

class SkateboardModel:
    def __init__(self, db_config: Dict):
        self.db_config = db_config
        self.conn = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(**self.db_config)
            return self
        except Exception as e:
            print(f"Error in __enter__: {str(e)}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            try:
                self.conn.close()
            except Exception as e:
                print(f"Error closing connection: {e}")
                pass

    def get_filtered_skateboards(self, weight: int, budget: float, purpose_id: int) -> List[Dict]:
        try:
            with self.conn.cursor() as cur:
                # SQL-запрос с использованием purpose_id
                sql_query = """
                    SELECT name, cost, ves, url, purposes, urlimage
                    FROM scates
                    WHERE ves >= %s
                      AND cost <= %s
                      AND purposes = %s
                    ORDER BY cost ASC
                    LIMIT 10;
                """
                print("SQL Query:", cur.mogrify(sql_query, (weight, budget, purpose_id)))
                cur.execute(sql_query, (weight, budget, purpose_id))
                columns = [desc[0] for desc in cur.description]
                results = []
                for row in cur.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
        except Exception as e:
            print(f"Error in get_filtered_skateboards: {str(e)}")
            raise