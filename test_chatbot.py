import json
import unittest
from app import app, kb, gemini_service

class TestSBJITMRChatbot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_knowledge_base_loaded(self):
        """Verify all 16 JSON knowledge files are loaded into memory."""
        self.assertGreaterEqual(len(kb.data), 16)
        self.assertIn("college", kb.data)
        self.assertIn("administration", kb.data)
        self.assertIn("deans", kb.data)
        self.assertIn("departments", kb.data)
        self.assertIn("placements", kb.data)
        self.assertIn("examinations", kb.data)
        self.assertIn("fees", kb.data)
        self.assertIn("scholarships", kb.data)

    def test_health_endpoint(self):
        """Test GET /api/health."""
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["knowledge_base_files_loaded"], 17)

    def ask(self, question: str, session_id: str = "test_suite"):
        res = self.client.post("/api/chat", json={"message": question, "session_id": session_id})
        self.assertEqual(res.status_code, 200)
        return res.get_json()

    # 0. Greeting test
    def test_q0_greeting(self):
        data = self.ask("hi")
        self.assertIn("Welcome to the **SBJITMR AI Assistant**", data["answer"])

    def test_q0_hello(self):
        data = self.ask("Hello there")
        self.assertIn("SBJITMR", data["answer"])

    # 1. Who is the Principal?
    def test_q1_principal(self):
        data = self.ask("Who is the Principal?")
        self.assertIn("Badjate", data["answer"])
        self.assertIn("principal@sbjit.edu.in", data["answer"])

    # 2. Who is the CEO?
    def test_q2_ceo(self):
        data = self.ask("Who is the CEO?")
        self.assertIn("Sanjeev Agrawal", data["answer"])
        self.assertIn("ceo@sbjit.edu.in", data["answer"])

    # 3. Who is the Dean Academics?
    def test_q3_dean_academics(self):
        data = self.ask("Who is the Dean Academics?")
        self.assertTrue("Pankaj" in data["answer"] and "Thote" in data["answer"])

    # 4. Who is the Dean Students Affairs?
    def test_q4_dean_students_affairs(self):
        data = self.ask("Who is the Dean Students Affairs?")
        self.assertIn("Yogesh", data["answer"])
        self.assertIn("Shinde", data["answer"])

    # 5. Who is the Dean Engineering?
    def test_q5_dean_engineering(self):
        data = self.ask("Who is the Dean Engineering?")
        self.assertIn("Raghuwanshi", data["answer"])

    # 6. Who is the CSE HOD?
    def test_q6_cse_hod(self):
        data = self.ask("Who is the CSE HOD?")
        self.assertIn("Anup Gade", data["answer"])

    # 7. What departments are available?
    def test_q7_departments_available(self):
        data = self.ask("What departments are available?")
        self.assertIn("Computer Science", data["answer"])
        self.assertIn("Electrical", data["answer"])
        self.assertIn("Mechanical", data["answer"])

    # 8. What courses are available?
    def test_q8_courses_available(self):
        data = self.ask("What courses are available?")
        self.assertIn("B.Tech", data["answer"])
        self.assertIn("MBA", data["answer"])

    # 9. What is the admission process?
    def test_q9_admission_process(self):
        data = self.ask("What is the admission process?")
        self.assertTrue("MHT-CET" in data["answer"] or "CAP" in data["answer"])

    # 10. What are the fees?
    def test_q10_fees(self):
        data = self.ask("What are the fees?")
        self.assertTrue("1,13,500" in data["answer"] or "FRA" in data["answer"])

    # 11. What scholarships are available?
    def test_q11_scholarships(self):
        data = self.ask("What scholarships are available?")
        self.assertIn("MahaDBT", data["answer"])
        self.assertIn("SC", data["answer"])
        self.assertIn("OBC", data["answer"])

    # 12. Where can I see exam results?
    def test_q12_exam_results(self):
        data = self.ask("Where can I check my exam results at SBJITMR?")
        self.assertIn("result.sbjit.edu.in", data["answer"])

    # 13. Where can I find exam timetable?
    def test_q13_exam_timetable(self):
        data = self.ask("Where can I find exam timetable?")
        self.assertIn("exam-time-table", data["answer"])

    # 14. Tell me about placements.
    def test_q14_placements(self):
        data = self.ask("Tell me about placements.")
        self.assertIn("12 LPA", data["answer"])
        self.assertIn("4.2 LPA", data["answer"])

    # 15. Who are the recruiters?
    def test_q15_recruiters(self):
        data = self.ask("Who are the recruiters?")
        self.assertTrue("TCS" in data["answer"] or "Capgemini" in data["answer"] or "Infosys" in data["answer"])

    # 16. Tell me about the library.
    def test_q16_library(self):
        data = self.ask("Tell me about the library.")
        self.assertIn("Prashant Wankhede", data["answer"])
        self.assertIn("OPAC", data["answer"])

    # 17. Tell me about transportation.
    def test_q17_transportation(self):
        data = self.ask("Tell me about transportation.")
        self.assertIn("20 buses", data["answer"])
        self.assertIn("Nagpur", data["answer"])

    # 18. What student activities are available?
    def test_q18_student_activities(self):
        data = self.ask("What student activities are available?")
        self.assertIn("ACES", data["answer"])
        self.assertIn("Technotsav", data["answer"])

    # 19. What is the vision and mission?
    def test_q19_vision_mission(self):
        data = self.ask("What is the vision and mission of SBJITMR?")
        self.assertIn("competent and creative", data["answer"])
        self.assertIn("academic excellence", data["answer"])

    # 20. When was SBJITMR established?
    def test_q20_established(self):
        data = self.ask("When was SBJITMR established?")
        self.assertIn("2008", data["answer"])
        self.assertIn("Badjate", data["answer"])

    # 21. What is the official contact number?
    def test_q21_contact_number(self):
        data = self.ask("What are the official contact numbers of SBJITMR?")
        self.assertIn("2667777", data["answer"])

    # 22. What is the official website?
    def test_q22_website(self):
        data = self.ask("What is the official website?")
        self.assertIn("sbjit.edu.in", data["answer"])

    # 23. Ask a question whose answer does not exist -> MUST NOT HALLUCINATE
    def test_q23_unverified_question_no_hallucination(self):
        data = self.ask("Who is the Head of Aerospace Engineering Department at SBJITMR?")
        self.assertIn("could not verify this information", data["answer"])
        self.assertIn("https://www.sbjit.edu.in/", data["answer"])

    # --- New Authoritative User Q&A Tests ---

    def test_new_mission(self):
        data = self.ask("What is the mission of SBJITMR?")
        self.assertIn("Providing Quality Infrastructure", data["answer"])

    def test_new_vision(self):
        data = self.ask("What is the vision of SBJITMR?")
        self.assertIn("competent and creative", data["answer"])

    def test_new_hod_bca_mca(self):
        data = self.ask("Who is the HOD of BCA / MCA at SBJITMR?")
        self.assertIn("Dr. Shailesh Gahane", data["answer"])
        self.assertIn("hodbca@sbjit.edu.in", data["answer"])

    def test_new_hod_bba(self):
        data = self.ask("Who is the HOD of BBA at SBJITMR?")
        self.assertIn("Department of Management", data["answer"])

    def test_new_intake_cse_core(self):
        data = self.ask("What is the intake of CSE (core) at SBJITMR?")
        self.assertIn("180 seats", data["answer"])

    def test_new_intake_cse_aiml(self):
        data = self.ask("What is the intake of CSE (AI & ML) at SBJITMR?")
        self.assertIn("60/120 seats", data["answer"])

    def test_new_intake_cse_ds(self):
        data = self.ask("What is the intake of CSE (Data Science) at SBJITMR?")
        self.assertIn("60 seats", data["answer"])

    def test_new_intake_etc(self):
        data = self.ask("What is the intake of E&TC at SBJITMR?")
        self.assertIn("60 seats", data["answer"])

    def test_new_intake_electrical(self):
        data = self.ask("What is the intake of Electrical Engineering at SBJITMR?")
        self.assertIn("60 seats", data["answer"])

    def test_new_intake_mechanical(self):
        data = self.ask("What is the intake of Mechanical Engineering at SBJITMR?")
        self.assertIn("60 seats", data["answer"])

    def test_new_intake_first_year(self):
        data = self.ask("What is the intake of First Year Engineering at SBJITMR?")
        self.assertIn("First Year Engineering", data["answer"])

    def test_new_intake_bca(self):
        data = self.ask("What is the intake of BCA at SBJITMR?")
        self.assertIn("Bachelor of Computer Application", data["answer"])

    def test_new_intake_mca(self):
        data = self.ask("What is the intake of MCA at SBJITMR?")
        self.assertIn("Master of Computer Application", data["answer"])

    def test_new_intake_mba(self):
        data = self.ask("What is the intake of MBA at SBJITMR?")
        self.assertIn("120 seats", data["answer"])

    def test_new_intake_btech_total(self):
        data = self.ask("What is the total B.Tech intake at SBJITMR?")
        self.assertIn("180", data["answer"])

    def test_new_intake_college_total(self):
        data = self.ask("What is the total college intake at SBJITMR?")
        self.assertIn("180", data["answer"])

    def test_new_governing_body(self):
        data = self.ask("What is the governing body of SBJITMR?")
        self.assertIn("Mr. Anuj Badjate", data["answer"])

    def test_new_exam_form_submission(self):
        data = self.ask("How do I submit my exam form at SBJITMR?")
        self.assertIn("Exam Form Registration", data["answer"])

    def test_new_revaluation_process(self):
        data = self.ask("How does the revaluation process work at SBJITMR?")
        self.assertIn("Grievance Form", data["answer"])

    def test_new_latest_admission_notice(self):
        data = self.ask("What is the latest admission notice published by SBJITMR?")
        self.assertIn("2026–27", data["answer"])
        self.assertIn("b-tech-first-year", data["answer"])

    def test_aniket_bhoyar(self):
        data = self.ask("who is aniket bhoyar he is cse faculty")
        self.assertIn("Aniket Bhoyar", data["answer"])
        self.assertIn("Assistant Professor", data["answer"])
        self.assertIn("Computer Science", data["answer"])

    def test_who_is_dean(self):
        data = self.ask("who is dean")
        self.assertIn("Pankaj", data["answer"])
        self.assertIn("Yogesh", data["answer"])
        self.assertIn("Raghuwanshi", data["answer"])

if __name__ == "__main__":
    unittest.main()
