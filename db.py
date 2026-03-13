import sqlite3

DB_NAME="expenses.db"
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL CHECK(amount >= 0),
            description TEXT NOT NULL CHECK(length(description) > 0),
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

    


def insert_expenses(amount,description):
   
    try:
        with sqlite3.connect(DB_NAME) as conn:
          cursor=conn.cursor()
          cursor.execute(
            """
            INSERT INTO expenses (amount, description,created_at)
            VALUES (?,?, datetime('now'))
            """,
            (amount,description)
        )

       
        return True, cursor.lastrowid

    
    except sqlite3.Error as e:
        return False , str(e)
    
  
def get_all_expenses():
   
    try:
        with sqlite3.connect(DB_NAME) as conn:
         cursor=conn.cursor()
         cursor.execute(
            """
            SELECT id, amount, description, created_at
            FROM expenses
            ORDER BY created_at DESC, id DESC

            """
        )

        rows = cursor.fetchall()

        expenses = []
        for row in rows:
            expenses.append({
                "id":row[0],
                "amount":row[1],
                "description":row[2],
                "created_at":row[3]

            })
        return True, expenses
    
    except sqlite3.Error as e:
        return False, str(e)
    

def delete_expense(expense_id):
    
    try:
       with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM expenses WHERE id = ?
        """,
        (expense_id,)
       )
       

       if cursor.rowcount==1:
              return "DELETED",None
       
       else:
           return "NOT_FOUND", None
    except sqlite3.Error as e:
         
          return "DB_ERROR", str(e)
        
   

def update_expense(expense_id,amount,description):

 try:
        with sqlite3.connect(DB_NAME) as conn:
         cursor=conn.cursor()
         cursor.execute(
            "SELECT id FROM expenses WHERE id=? ",
             (expense_id,)
        )
        row = cursor.fetchone()

        if not row:
            return "NOT_FOUND",None
        
        cursor.execute(
            """
            UPDATE expenses
            SET amount=?,description = ?
            WHERE id =?
            
            """,
            (amount, description,expense_id)
        )
        return "UPDATED",None
    
 except sqlite3.Error as e:
        return "DB_ERROR" ,str(e)
 
 