from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://chakmake_businessdb:Maheshraj##123@23.106.53.56/chakmake_business_profile?charset=utf8mb4"

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
    
def load_business_to_db(bp_dict):
   with engine.connect() as conn:
      try:
         result = conn.execute(text(f"INSERT INTO business_profile(business_name, panvat, proprietor, address, est_year, description, service1, service1_desc, service2, service2_desc, service3, service3_desc, service4, service4_desc) VALUES (:v1, :v2, :v3, :v4, :v5, :v6, :v7, :v8, :v9, :v10, :v11, :v12, :v13, :v14)"),
                {"v1": bp_dict["business_name"], "v2": bp_dict["panvat"], "v3": bp_dict["proprietor"], "v4": bp_dict["address"], "v5": bp_dict["est_year"], "v6": bp_dict["description"], "v7": bp_dict["service1"], "v8": bp_dict["service1_desc"], "v9": bp_dict["service2"], "v10": bp_dict["service2_desc"], "v11": bp_dict["service3"], "v12": bp_dict["service3_desc"], "v13": bp_dict["service4"], "v14": bp_dict["service4_desc"]})
         return True
      except:
         return False