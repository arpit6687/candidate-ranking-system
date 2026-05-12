from models.admin import AdminModel
from models.candidate import CandidateModel

def run_seed():
    print("Seeding Administrator...")
    AdminModel.create_admin('admin', 'admin123')
    
    print("Seeding Candidates...")
    candidates = [
        ("Alice Cooper", "alice@example.com", 85, 90, 5, 88),
        ("Bob Builder", "bob@example.com", 70, 75, 2, 70),
        ("Charlie Chaplin", "charlie@example.com", 95, 80, 8, 92),
        ("Diana Prince", "diana@example.com", 100, 95, 12, 98),
        ("Eve Polastri", "eve@example.com", 60, 65, 1, 60),
        ("Frank Castle", "frank@example.com", 80, 88, 7, 85)
    ]
    
    for name, email, ac, sk, exp, test in candidates:
        try:
            CandidateModel.add_candidate(name, email, ac, sk, exp, test)
            print(f"Added {name}")
        except Exception as e:
            print(f"Skipping {name} (may already exist).")
            
    print("Seed complete.")

if __name__ == '__main__':
    run_seed()
