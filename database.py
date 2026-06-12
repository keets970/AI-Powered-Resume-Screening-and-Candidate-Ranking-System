import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root", 
        database="resume_screener"
    )

def save_job(title, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO jobs (title, description) VALUES (%s, %s)",
        (title, description)
    )
    conn.commit()
    job_id = cursor.lastrowid
    conn.close()
    return job_id

def save_candidate(job_id, name, email, skills, score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO candidates (job_id, name, email, skills, score) VALUES (%s, %s, %s, %s, %s)",
        (job_id, name, email, ", ".join(skills), score)
    )
    conn.commit()
    conn.close()

def get_candidates(job_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, email, skills, score FROM candidates WHERE job_id=%s ORDER BY score DESC",
        (job_id,)
    )
    results = cursor.fetchall()
    conn.close()
    return results

# TEST
if __name__ == "__main__":
    job_id = save_job("Python Developer", "Looking for Python ML developer")
    save_candidate(job_id, "Alex Morgan", "alex@email.com", ["python", "sql", "ml"], 41.94)
    print("Saved successfully!")
    print(get_candidates(job_id))