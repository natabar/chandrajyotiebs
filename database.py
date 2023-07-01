from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://chakmake_cjadmin:Maheshraj##123@23.106.53.56/chakmake_cjschool?charset=utf8mb4"

engine = create_engine(
    db_connection_string,
    connect_args={
    "ssl":{
    "ssl_ca": "/etc/ssl/cert.pem",
    }
    })

def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        jobs = []
        for row in result.all():
            jobs.append(row._asdict())
        return jobs

def load_notices_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from newsandupdates"))
        notices = []
        for row in result.all():
            notices.append(row._asdict())
        return notices

def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(
      text(f"SELECT * FROM jobs WHERE id = :val"),
      {"val": id}
    )
    rows = result.mappings().all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0])

def load_notice_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(
      text(f"SELECT * FROM newsandupdates WHERE id = :val"),
      {"val": id}
    )
    rows = result.mappings().all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0])
