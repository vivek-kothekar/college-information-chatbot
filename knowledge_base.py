import os
import json
import re
from typing import Dict, Any, List, Optional, Tuple

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

class KnowledgeBase:
    """
    Structured in-memory Knowledge Base loader and intelligent retriever
    for S. B. Jain Institute of Technology, Management & Research (SBJITMR).
    """

    def __init__(self, data_dir: str = DATA_DIR):
        self.data_dir = data_dir
        self.data: Dict[str, Any] = {}
        self.load_all()

    def load_all(self):
        """Loads all 16 JSON knowledge files into memory."""
        files = [
            "college.json", "administration.json", "deans.json", "departments.json",
            "faculty.json", "admissions.json", "fees.json", "scholarships.json",
            "examinations.json", "placements.json", "facilities.json",
            "student_activities.json", "committees.json", "contacts.json",
            "important_links.json", "sources.json", "qa_pairs.json"
        ]
        for f in files:
            p = os.path.join(self.data_dir, f)
            key = f.replace(".json", "")
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as fp:
                        self.data[key] = json.load(fp)
                except Exception as e:
                    print(f"Error loading {f}: {e}")
                    self.data[key] = {}
            else:
                self.data[key] = {}

    def get_full_context_summary(self) -> str:
        """Returns a condensed text digest of the entire knowledge base for Gemini grounding."""
        summary_parts = []
        
        # College summary
        c = self.data.get("college", {})
        summary_parts.append(
            f"INSTITUTE: {c.get('institute_name', {}).get('full_name')} ({c.get('institute_name', {}).get('short_name')})\n"
            f"Location: {c.get('campus_and_infrastructure', {}).get('location')}\n"
            f"Established: {c.get('establishment', {}).get('year')} by {c.get('establishment', {}).get('founder_trust')}\n"
            f"Affiliation & Approvals: {c.get('status_and_approvals', {}).get('autonomous_status')}, affiliated to {c.get('status_and_approvals', {}).get('affiliating_university')}, approved by {c.get('status_and_approvals', {}).get('approvals')}, DTE Code: {c.get('status_and_approvals', {}).get('dte_code')}, NAAC Grade: {c.get('status_and_approvals', {}).get('accreditation')}.\n"
            f"Vision: {c.get('vision', {}).get('statement')}\n"
            f"Mission: {'; '.join(c.get('mission', {}).get('points', []))}\n"
            f"Official Website: {c.get('official_contacts', {}).get('website')}, Email: {c.get('official_contacts', {}).get('general_enquiry_email')}, Phone: {c.get('official_contacts', {}).get('telephone')}"
        )

        # Administration & Deans
        adm = self.data.get("administration", {})
        summary_parts.append("\nTOP LEADERSHIP & DEANS:")
        for role_key, person in adm.items():
            summary_parts.append(
                f"- {person.get('designation')}: {person.get('name')} | Email: {person.get('email')} | Phone: {person.get('phone')} | Office: {person.get('department_or_office')} | Source: {person.get('source')}"
            )

        # Deans detail
        deans = self.data.get("deans", {})
        for d_key, d in deans.items():
            resp = ", ".join(d.get("responsibilities", []))
            summary_parts.append(
                f"- {d.get('designation')}: {d.get('name')} | Email: {d.get('email')} | Phone: {d.get('phone')} | Role: {d.get('role')} | Key Responsibilities: {resp} | Source: {d.get('source')}"
            )

        # Departments & HODs
        depts = self.data.get("departments", {})
        summary_parts.append("\nDEPARTMENTS & HODS:")
        for d_key, d in depts.items():
            hod = d.get("hod", {})
            progs = ", ".join(d.get("programs_offered", []))
            summary_parts.append(
                f"- {d.get('name')} ({d.get('short_name', '')}): HOD: {hod.get('name', 'N/A')} (Email: {hod.get('email', 'N/A')}, Phone: {hod.get('phone', 'N/A')}) | Programs: {progs} | URL: {d.get('url', '')}"
            )

        # Admissions & Helpline
        adm_info = self.data.get("admissions", {})
        helpline = adm_info.get("admission_helpline", {})
        phones = ", ".join(helpline.get("phone_numbers", []))
        summary_parts.append(
            f"\nADMISSIONS (DTE Code: 4197):\n"
            f"Helpline: Incharge {helpline.get('incharge')}, Numbers: {phones}, WhatsApp: {helpline.get('whatsapp')}, Email: {helpline.get('email')}.\n"
            f"Admissions are via CAP by State CET Cell Maharashtra (MHT-CET / JEE Main for B.Tech; MAH-CET for MBA/BCA/BBA/MCA)."
        )

        # Fees & NEFT
        fees = self.data.get("fees", {})
        neft = fees.get("bank_neft_rtgs_details", {})
        summary_parts.append(
            f"\nFEES & BANK DETAILS:\n"
            f"Fees are regulated by Fee Regulating Authority (FRA) Maharashtra.\n"
            f"B.Tech approx ~₹1.20L-₹1.27L/year (~₹5.08 Lakhs for 4 years for Open; 50% concession for OBC/EBC via MahaDBT; 100% concession for SC/ST via GOI scholarship).\n"
            f"MBA approx ~₹1.00L/year (~₹2.01 Lakhs total).\n"
            f"Bank Details: Name: {neft.get('account_name')}, A/C: {neft.get('account_number')}, IFSC: {neft.get('ifsc_code')}, Bank: {neft.get('bank_name')} ({neft.get('branch')}). DD in favor of \"S. B. Jain Institute of Technology, Management & Research\" payable at NAGPUR. Confirmation: 9921021167 / 7507684984."
        )

        # Scholarships
        sch = self.data.get("scholarships", {})
        summary_parts.append("\nSCHOLARSHIPS (MahaDBT & Central):")
        for s in sch.get("government_scholarship_schemes", []):
            summary_parts.append(
                f"- Category: {s.get('category')} | Scheme: {s.get('scheme')} | Income: {s.get('income_limit')} | Benefit: {s.get('benefit')} | Portal: {s.get('where_to_apply')}"
            )

        # Examinations
        exam = self.data.get("examinations", {})
        coe = exam.get("examination_cell", {}).get("controller_of_examinations", {})
        cgpa = exam.get("cgpa_to_percentage_conversion", {})
        summary_parts.append(
            f"\nEXAMINATION SYSTEM:\n"
            f"Autonomous Examination Cell headed by CoE {coe.get('name')} (Email: {coe.get('email')}).\n"
            f"Results, timetable, forms, and revaluation available on official portal: https://www.sbjit.edu.in/exam-cell/\n"
            f"CGPA to Percentage Formula: {cgpa.get('formula')} (or CGPA * 10)."
        )

        # Placements
        plc = self.data.get("placements", {})
        stats = plc.get("placement_statistics", {})
        tpo = plc.get("training_and_placement_cell", {}).get("head_tpo", {})
        recs = ", ".join(plc.get("top_recruiters", [])[:12])
        summary_parts.append(
            f"\nPLACEMENTS:\n"
            f"Highest Package: {stats.get('highest_package')}, Average Package: {stats.get('average_package')}, 3500+ students placed across 600+ companies.\n"
            f"Head T&P: {tpo.get('name')} (Contact: {tpo.get('contact')}, Email: {tpo.get('email')}).\n"
            f"Top Recruiters: {recs}.\n"
            f"Official Placements Link: https://www.sbjit.edu.in/placements/"
        )

        # Facilities
        fac = self.data.get("facilities", {})
        lib = fac.get("central_library", {})
        trans = fac.get("transportation", {})
        summary_parts.append(
            f"\nCAMPUS FACILITIES:\n"
            f"- Library: {lib.get('name')} - computerized, Web OPAC, Book Bank for all students, NPTEL, J-Gate, Librarian: Mr. Prashant Wankhede. URL: https://www.sbjit.edu.in/s-b-jain-library/\n"
            f"- Transportation: 20 buses covering Nagpur, Kamptee, Saoner (arrives 10:00 AM, departs 5:30 PM), GPS, speed governors, emergency door, 24/7 on-campus emergency vehicle. URL: https://www.sbjit.edu.in/transportation/\n"
            f"- Sports & Gym: Gymnasium, sports ground for cricket, basketball, volleyball, indoor games.\n"
            f"- Power Backup: 100% DG generator backup."
        )

        # Student Activities
        act = self.data.get("student_activities", {})
        summary_parts.append(
            f"\nSTUDENT ACTIVITIES:\n"
            f"Under Dean Students Affairs Dr. Yogesh P. Shinde. NSS Unit conducts 7-day rural camp, blood donation, Swachh Bharat. Sports Cell led by Mr. Ajay Joshi. Annual Tech Fest: Technotsav; Cultural Fest: Manthan. Forums: ACES (CSE), MESA (Mech), ELESA (EE), IEEE."
        )

        # Academic Council & Governance
        com = self.data.get("committees", {})
        council = com.get("academic_council", {})
        summary_parts.append(
            f"\nGOVERNANCE & COMMITTEES:\n"
            f"Academic Council Chairman: {council.get('chairman')}, Member Secretary: {council.get('member_secretary')}. Composed of 21 members including RTMNU university nominees, VNIT educationalists, industry representatives, all HODs, and Deans. URL: https://www.sbjit.edu.in/academic-council/"
        )

        return "\n".join(summary_parts)

    def query_local_kb(self, query: str, return_flag: bool = False) -> Any:
        """
        Intelligent local entity/topic matcher that synthesizes clean, verified answers
        directly from the JSON files according to the prompt instructions.
        Returns (answer_markdown, sources_list) or (answer_markdown, sources_list, is_authoritative).
        """
        def _ret(ans, src, is_auth=False):
            return (ans, src, is_auth) if return_flag else (ans, src)

        q = query.lower().strip()
        # Clean punctuation for exact word matching
        q_clean = re.sub(r'[^a-zA-Z0-9\s]', '', q).strip()
        sources = []

        # 0. Conversational Greetings & Identity
        greetings = ["hi", "hello", "hey", "namaste", "good morning", "good afternoon", "good evening", "greetings", "hi there", "hello there"]
        if q_clean in greetings or q_clean.startswith("hi ") or q_clean.startswith("hello "):
            sources.append({"title": "Official SBJITMR Website", "url": "https://www.sbjit.edu.in/"})
            ans = (
                "Hello! Welcome to the **SBJITMR AI Assistant**.\n\n"
                "I am here to help you with complete, verified information about **S. B. Jain Institute of Technology, Management & Research (SBJITMR), Nagpur**.\n\n"
                "You can ask me about:\n"
                "- **Administration:** Principal, CEO, Deans, Registrar, and HODs\n"
                "- **Admissions & Fees:** Eligibility, CAP rounds, fee structure, and NEFT details\n"
                "- **Courses & Departments:** B.Tech (CSE, AIML, Data Science, EE, ETC, Mech), MBA, MCA, BCA, BBA\n"
                "- **Placements:** Highest package (12 LPA), average package (4.2 LPA), and top recruiters\n"
                "- **Examinations & Scholarships:** Result portal, timetable, MahaDBT schemes\n"
                "- **Campus Facilities:** 20 college buses, library, and sports\n\n"
                "What would you like to know?"
            )
            return _ret(ans, sources, is_auth=True)

        if any(w in q_clean for w in ["who are you", "what are you", "what can you do", "help me", "how can you help"]):
            sources.append({"title": "Official SBJITMR Website", "url": "https://www.sbjit.edu.in/"})
            ans = (
                "I am the **SBJITMR AI Assistant**, dedicated to answering your questions about **S. B. Jain Institute of Technology, Management & Research (SBJITMR), Nagpur**.\n\n"
                "All information is directly verified from official SBJITMR pages and documents with zero hallucination. Feel free to ask any question about admissions, fees, departments, faculty, placements, or campus facilities!"
            )
            return _ret(ans, sources, is_auth=True)

        if q_clean in ["thank you", "thanks", "thanks a lot", "thank you so much", "bye", "goodbye", "see you"]:
            sources.append({"title": "Official SBJITMR Website", "url": "https://www.sbjit.edu.in/"})
            return _ret("You're very welcome! If you have any further questions about SBJITMR, I'm always here to help. Have a wonderful day!", sources, is_auth=True)

        # Check explicit Q&A Pairs
        qa_pairs = self.data.get("qa_pairs", [])
        if qa_pairs and isinstance(qa_pairs, list):
            # 1. Exact match on normalized text
            for item in qa_pairs:
                for q_text in item.get("questions", []):
                    q_text_clean = re.sub(r'[^a-zA-Z0-9\s]', '', q_text).lower().strip()
                    if q_clean == q_text_clean:
                        return _ret(item["answer"], item.get("sources", []), is_auth=True)

            # 2. Substring match with longest match specificity
            best_match = None
            best_sub_len = 0
            for item in qa_pairs:
                for q_text in item.get("questions", []):
                    q_text_clean = re.sub(r'[^a-zA-Z0-9\s]', '', q_text).lower().strip()
                    if (len(q_clean) > 8 and q_clean in q_text_clean) or (len(q_text_clean) > 8 and q_text_clean in q_clean):
                        match_len = min(len(q_clean), len(q_text_clean))
                        if match_len > best_sub_len:
                            best_sub_len = match_len
                            best_match = item
            if best_match:
                return _ret(best_match["answer"], best_match.get("sources", []), is_auth=True)

            # 3. High confidence token overlap match
            stop_words = {"what", "is", "the", "at", "of", "in", "for", "and", "a", "an", "to", "who", "when", "does", "how", "sbjitmr", "sbjit", "jain", "college", "institute", "tell", "me", "about"}
            q_tokens = set(q_clean.split()) - stop_words
            if len(q_tokens) >= 2:
                best_item = None
                best_score = 0.0
                for item in qa_pairs:
                    for q_text in item.get("questions", []):
                        target_clean = re.sub(r'[^a-zA-Z0-9\s]', '', q_text).lower().strip()
                        target_tokens = set(target_clean.split()) - stop_words
                        if not target_tokens:
                            continue
                        common = q_tokens.intersection(target_tokens)
                        overlap_ratio = len(common) / len(target_tokens)
                        query_overlap = len(common) / len(q_tokens)
                        score = 2 * (overlap_ratio * query_overlap) / (overlap_ratio + query_overlap) if (overlap_ratio + query_overlap) > 0 else 0
                        if score > best_score and score >= 0.7:
                            best_score = score
                            best_item = item
                if best_item:
                    return _ret(best_item["answer"], best_item.get("sources", []), is_auth=True)

        # 1. Principal
        if any(w in q for w in ["principal", "director", "head of institute", "head of the institute"]):
            p = self.data.get("administration", {}).get("principal", {})
            sources.append({"title": "Official SBJITMR Principal Message", "url": p.get("source", "https://www.sbjit.edu.in/message-from-principal/")})
            ans = (
                f"### Principal\n\n"
                f"**Name:** {p.get('name')}\n\n"
                f"**Designation:** {p.get('designation')}\n\n"
                f"**Office:** {p.get('department_or_office')}\n\n"
                f"**Email:** {p.get('email')}\n\n"
                f"**Phone:** {p.get('phone')}\n\n"
                f"**Responsibilities:**\n"
                f"- Institutional leadership and academic administration\n"
                f"- Presiding Chairman of the Academic Council\n"
                f"- Statutory compliance and quality assurance\n\n"
                f"**Source:** [Official SBJITMR Message from Principal]({p.get('source')})"
            )
            return ans, sources

        # 2. CEO
        if any(w in q for w in ["ceo", "chief executive officer"]):
            ceo = self.data.get("administration", {}).get("ceo", {})
            sources.append({"title": "Official SBJITMR CEO Message", "url": ceo.get("source", "https://www.sbjit.edu.in/message-from-ceo/")})
            ans = (
                f"### Chief Executive Officer (CEO)\n\n"
                f"**Name:** {ceo.get('name')}\n\n"
                f"**Designation:** {ceo.get('designation')}\n\n"
                f"**Office:** {ceo.get('department_or_office')}\n\n"
                f"**Email:** {ceo.get('email')}\n\n"
                f"**Phone:** {ceo.get('phone')}\n\n"
                f"**Responsibilities:**\n"
                f"- Executive management and strategic institutional growth\n"
                f"- Industry partnerships and corporate relations\n"
                f"- Infrastructure and resource development\n\n"
                f"**Source:** [Official SBJITMR Message from CEO]({ceo.get('source')})"
            )
            return ans, sources

        # 3. Dean Academics
        if "dean academic" in q or "dean academics" in q:
            d = self.data.get("deans", {}).get("dean_academics", {})
            sources.append({"title": "Official SBJITMR Dean Academics Message", "url": d.get("source", "https://www.sbjit.edu.in/message-from-dean-academics/")})
            resp_list = "\n".join([f"- {r}" for r in d.get("responsibilities", [])])
            ans = (
                f"### Dean Academics\n\n"
                f"**Name:** {d.get('name')}\n\n"
                f"**Role:** {d.get('role')}\n\n"
                f"**Office:** {d.get('office')}\n\n"
                f"**Email:** {d.get('email')}\n\n"
                f"**Phone:** {d.get('phone')}\n\n"
                f"**Responsibilities:**\n"
                f"{resp_list}\n\n"
                f"**Source:** [Official SBJITMR Dean Academics]({d.get('source')})"
            )
            return ans, sources

        # 4. Dean Students Affairs / Student Affairs
        if "dean student" in q or "dean students" in q or "dean student affairs" in q:
            d = self.data.get("deans", {}).get("dean_students_affairs", {})
            sources.append({"title": "Official SBJITMR Student Affairs", "url": d.get("source", "https://www.sbjit.edu.in/student-affairs/")})
            resp_list = "\n".join([f"- {r}" for r in d.get("responsibilities", [])])
            ans = (
                f"### Dean Students Affairs\n\n"
                f"**Name:** {d.get('name')}\n\n"
                f"**Role:** {d.get('role')}\n\n"
                f"**Office:** {d.get('office')}\n\n"
                f"**Email:** {d.get('email')}\n\n"
                f"**Phone:** {d.get('phone')}\n\n"
                f"**Responsibilities:**\n"
                f"{resp_list}\n\n"
                f"**Source:** [Official SBJITMR Student Affairs]({d.get('source')})"
            )
            return ans, sources

        # 5. Dean Engineering
        if "dean engineering" in q:
            d = self.data.get("deans", {}).get("dean_engineering", {})
            sources.append({"title": "Official SBJITMR Academic Council", "url": d.get("source", "https://www.sbjit.edu.in/academic-council/")})
            resp_list = "\n".join([f"- {r}" for r in d.get("responsibilities", [])])
            ans = (
                f"### Dean Engineering\n\n"
                f"**Name:** {d.get('name')}\n\n"
                f"**Role:** {d.get('role')}\n\n"
                f"**Office:** {d.get('office')}\n\n"
                f"**Email:** {d.get('email')}\n\n"
                f"**Phone:** {d.get('phone')}\n\n"
                f"**Responsibilities:**\n"
                f"{resp_list}\n\n"
                f"**Source:** [Official SBJITMR Academic Council]({d.get('source')})"
            )
            return ans, sources

        # 6. Dean R&D / Research
        if "dean research" in q or "dean r&d" in q or "dean rd" in q:
            d = self.data.get("deans", {}).get("dean_research_development", {})
            sources.append({"title": "Official SBJITMR R&D Cell", "url": d.get("source", "https://www.sbjit.edu.in/rd-cell/")})
            resp_list = "\n".join([f"- {r}" for r in d.get("responsibilities", [])])
            ans = (
                f"### Dean (Research & Development)\n\n"
                f"**Name:** {d.get('name')}\n\n"
                f"**Role:** {d.get('role')}\n\n"
                f"**Office:** {d.get('office')}\n\n"
                f"**Email:** {d.get('email')}\n\n"
                f"**Phone:** {d.get('phone')}\n\n"
                f"**Responsibilities:**\n"
                f"{resp_list}\n\n"
                f"**Source:** [Official SBJITMR R&D Cell]({d.get('source')})"
            )
            return ans, sources

        # 7. General Deans Query ("who is dean", "deans", "who are the deans")
        if "dean" in q or "deans" in q:
            sources.append({"title": "Official SBJITMR Dean Academics", "url": "https://www.sbjit.edu.in/message-from-dean-academics/"})
            sources.append({"title": "Official SBJITMR Student Affairs", "url": "https://www.sbjit.edu.in/student-affairs/"})
            sources.append({"title": "Official SBJITMR Academic Council", "url": "https://www.sbjit.edu.in/academic-council/"})
            ans = (
                "### Deans at SBJITMR\n\n"
                "S. B. Jain Institute of Technology, Management & Research (SBJITMR), Nagpur has dedicated deans heading academic and student administration:\n\n"
                "1. **Dean Academics:** **Dr. Pankaj B. Thote**\n"
                "   - **Email:** `deanacademics@sbjit.edu.in`\n"
                "   - **Role:** Oversees academic regulations, curriculum execution, and autonomous academic standards.\n\n"
                "2. **Dean Students Affairs:** **Dr. Yogesh P. Shinde**\n"
                "   - **Email:** `deanstudentsaffairs@sbjit.edu.in` | **Phone:** +91 9923280550, +91 8999300998\n"
                "   - **Role:** Heads student welfare, NSS cell, clubs, sports, discipline, and campus life.\n\n"
                "3. **Dean Engineering:** **Dr. M. M. Raghuwanshi**\n"
                "   - **Role:** Teacher's Representative in Academic Council, oversees technical engineering programs.\n\n"
                "**Sources:**\n"
                "- [Dean Academics Desk](https://www.sbjit.edu.in/message-from-dean-academics/)\n"
                "- [Dean Students Affairs Desk](https://www.sbjit.edu.in/student-affairs/)"
            )
            return _ret(ans, sources, is_auth=True)

        # Registrar
        if "registrar" in q:
            r = self.data.get("administration", {}).get("registrar", {})
            sources.append({"title": "Official SBJITMR Administration", "url": r.get("source", "https://www.sbjit.edu.in/contact-us/")})
            ans = (
                f"### Registrar & Administration\n\n"
                f"**Office:** {r.get('department_or_office')}\n\n"
                f"**Designation:** {r.get('designation')}\n\n"
                f"**Email:** {r.get('email')}\n\n"
                f"**Phone:** {r.get('phone')}\n\n"
                f"**Key Responsibilities:** {r.get('responsibilities')}\n\n"
                f"**Source:** [Official SBJITMR Contact Page]({r.get('source')})"
            )
            return ans, sources

        # Controller of Examination / COE
        if "controller of exam" in q or "coe" in q or "controller of examination" in q:
            coe = self.data.get("administration", {}).get("controller_of_examinations", {})
            sources.append({"title": "Official SBJITMR Exam Cell", "url": coe.get("source", "https://www.sbjit.edu.in/exam-cell/")})
            ans = (
                f"### Controller of Examinations (CoE)\n\n"
                f"**Name:** {coe.get('name')}\n\n"
                f"**Designation:** {coe.get('designation')}\n\n"
                f"**Office:** {coe.get('department_or_office')}\n\n"
                f"**Email:** {coe.get('email')}\n\n"
                f"**Phone:** {coe.get('phone')}\n\n"
                f"**Responsibilities:** {coe.get('responsibilities')}\n\n"
                f"**Source:** [Official SBJITMR Exam Cell]({coe.get('source')})"
            )
            return ans, sources

        # HOD CSE
        if "cse hod" in q or ("hod" in q and "computer science" in q and "ai" not in q and "data" not in q):
            dept = self.data.get("departments", {}).get("computer_science_engineering", {})
            hod = dept.get("hod", {})
            sources.append({"title": "Official SBJITMR CSE Department", "url": dept.get("url", "https://www.sbjit.edu.in/computer-science-and-engineering/")})
            ans = (
                f"### Head of Department - Computer Science & Engineering (CSE)\n\n"
                f"**Name:** {hod.get('name')}\n\n"
                f"**Designation:** {hod.get('designation')}\n\n"
                f"**Email:** {hod.get('email')}\n\n"
                f"**Department:** {dept.get('name')}\n\n"
                f"**Phone:** {hod.get('phone')}\n\n"
                f"**Source:** [Official SBJITMR CSE Department]({dept.get('url')})"
            )
            return ans, sources

        # HOD CSE AI & ML
        if ("ai" in q and "ml" in q and "hod" in q) or "hod aiml" in q:
            dept = self.data.get("departments", {}).get("cse_aiml", {})
            hod = dept.get("hod", {})
            sources.append({"title": "Official SBJITMR Emerging Technologies", "url": dept.get("url", "https://www.sbjit.edu.in/emerging-technologies/")})
            ans = (
                f"### Head of Department - CSE (AI & ML)\n\n"
                f"**Name:** {hod.get('name')}\n\n"
                f"**Designation:** {hod.get('designation')}\n\n"
                f"**Email:** {hod.get('email')}\n\n"
                f"**Department:** {dept.get('name')}\n\n"
                f"**Source:** [Official SBJITMR Emerging Technologies]({dept.get('url')})"
            )
            return ans, sources

        # HOD Data Science
        if ("data science" in q and "hod" in q) or "hod ds" in q:
            dept = self.data.get("departments", {}).get("cse_data_science", {})
            hod = dept.get("hod", {})
            sources.append({"title": "Official SBJITMR CSE Data Science", "url": dept.get("url", "https://www.sbjit.edu.in/cseds-home/")})
            ans = (
                f"### Head of Department - CSE (Data Science)\n\n"
                f"**Name:** {hod.get('name')}\n\n"
                f"**Designation:** {hod.get('designation')}\n\n"
                f"**Email:** {hod.get('email')}\n\n"
                f"**Department:** {dept.get('name')}\n\n"
                f"**Source:** [Official SBJITMR Data Science]({dept.get('url')})"
            )
            return ans, sources

        # Other HODs
        if "electrical" in q and "hod" in q:
            dept = self.data.get("departments", {}).get("electrical_engineering", {})
            hod = dept.get("hod", {})
            sources.append({"title": "Official SBJITMR Electrical Engg", "url": dept.get("url", "https://www.sbjit.edu.in/electrical-engineering/")})
            return f"### Head of Department - Electrical Engineering\n\n**Name:** {hod.get('name')}\n**Designation:** {hod.get('designation')}\n**Email:** {hod.get('email')}\n**Source:** [Official SBJITMR Electrical]({dept.get('url')})", sources

        if ("mechanical" in q or "mech" in q) and "hod" in q:
            dept = self.data.get("departments", {}).get("mechanical_engineering", {})
            hod = dept.get("hod", {})
            sources.append({"title": "Official SBJITMR Mechanical Engg", "url": dept.get("url", "https://www.sbjit.edu.in/mechanical-engineering/")})
            return f"### Head of Department - Mechanical Engineering\n\n**Name:** {hod.get('name')}\n**Designation:** {hod.get('designation')}\n**Email:** {hod.get('email')}\n**Source:** [Official SBJITMR Mechanical]({dept.get('url')})", sources

        if ("etc" in q or "electronics" in q) and "hod" in q:
            dept = self.data.get("departments", {}).get("electronics_and_telecommunication", {})
            hod = dept.get("hod", {})
            sources.append({"title": "Official SBJITMR ETC Department", "url": dept.get("url", "https://www.sbjit.edu.in/electronicsandtele/")})
            return f"### Head of Department - Electronics & Telecommunication Engineering\n\n**Name:** {hod.get('name')}\n**Designation:** {hod.get('designation')}\n**Email:** {hod.get('email')}\n**Source:** [Official SBJITMR ETC]({dept.get('url')})", sources

        if "mba" in q and "hod" in q:
            dept = self.data.get("departments", {}).get("master_of_business_administration", {})
            hod = dept.get("hod", {})
            sources.append({"title": "Official SBJITMR MBA Department", "url": dept.get("url", "https://www.sbjit.edu.in/mba/")})
            return f"### Head of Department - Management Studies (MBA)\n\n**Name:** {hod.get('name')}\n**Designation:** {hod.get('designation')}\n**Email:** {hod.get('email')}\n**Source:** [Official SBJITMR MBA]({dept.get('url')})", sources

        # Departments available / Courses offered
        if any(w in q for w in ["what departments", "departments available", "list of departments", "what courses", "courses are offered", "courses offered", "programs offered"]):
            depts = self.data.get("departments", {})
            sources.append({"title": "Official SBJITMR Degree Programs", "url": "https://www.sbjit.edu.in/programs/"})
            ans = (
                f"### Academic Departments & Programs Offered at SBJITMR\n\n"
                f"S. B. Jain Institute of Technology, Management & Research offers the following approved programs:\n\n"
                f"#### Undergraduate Programs (B.Tech - 4 Years):\n"
                f"- **Computer Science & Engineering (CSE)** (Intake: 180)\n"
                f"- **CSE (Artificial Intelligence & Machine Learning)** (Intake: 60/120)\n"
                f"- **CSE (Data Science)** (Intake: 60)\n"
                f"- **Electrical Engineering** (Intake: 60)\n"
                f"- **Electronics & Telecommunication Engineering** (Intake: 60)\n"
                f"- **Mechanical Engineering** (Intake: 60)\n"
                f"- **Direct Second Year B.Tech (Lateral Entry)** for Diploma holders\n\n"
                f"#### Undergraduate Applied & Management Programs:\n"
                f"- **Bachelor of Computer Application (BCA)** (3 Years)\n"
                f"- **Bachelor of Business Administration (BBA)** (3 Years)\n\n"
                f"#### Postgraduate Programs:\n"
                f"- **Master of Business Administration (MBA)** (2 Years, Intake: 120)\n"
                f"- **Master of Computer Application (MCA)** (2 Years)\n"
                f"- **M.Tech in Computer Science & Engineering** (2 Years)\n"
                f"- **M.Tech in Electronics / VLSI** (2 Years)\n\n"
                f"**Source:** [Official SBJITMR Programs Guide](https://www.sbjit.edu.in/programs/)"
            )
            return ans, sources

        # Specific Department Queries: CSE, CSE AIML, Data Science, MBA
        if "what is the cse department" in q or "tell me about cse" in q or ("about" in q and "cse department" in q):
            d = self.data.get("departments", {}).get("computer_science_engineering", {})
            sources.append({"title": "Official SBJITMR CSE Department", "url": d.get("url")})
            labs = "\n".join([f"- {l}" for l in d.get("labs", [])])
            return (
                f"### Department of Computer Science & Engineering (CSE)\n\n"
                f"{d.get('description')}\n\n"
                f"**HOD:** {d.get('hod', {}).get('name')} (Email: {d.get('hod', {}).get('email')})\n\n"
                f"**Programs:** {', '.join(d.get('programs_offered', []))}\n\n"
                f"**Key Laboratories:**\n{labs}\n\n"
                f"**Placement Highlights:** {d.get('placement_highlights')}\n\n"
                f"**Source:** [Official SBJITMR CSE Department]({d.get('url')})"
            ), sources

        if "ai & ml" in q or "aiml" in q or "artificial intelligence" in q:
            d = self.data.get("departments", {}).get("cse_aiml", {})
            sources.append({"title": "Official SBJITMR Emerging Technologies", "url": d.get("url")})
            labs = "\n".join([f"- {l}" for l in d.get("labs", [])])
            return (
                f"### Department of CSE (Artificial Intelligence & Machine Learning)\n\n"
                f"{d.get('description')}\n\n"
                f"**HOD:** {d.get('hod', {}).get('name')} (Email: {d.get('hod', {}).get('email')})\n\n"
                f"**Key Features:** GPU-enabled high performance computing lab, specialized training in PyTorch, TensorFlow, Computer Vision, and Generative AI.\n\n"
                f"**Laboratories:**\n{labs}\n\n"
                f"**Source:** [Official SBJITMR Emerging Technologies]({d.get('url')})"
            ), sources

        if "data science" in q and not ("hod" in q and "who" in q):
            d = self.data.get("departments", {}).get("cse_data_science", {})
            sources.append({"title": "Official SBJITMR Data Science", "url": d.get("url")})
            labs = "\n".join([f"- {l}" for l in d.get("labs", [])])
            return (
                f"### Department of CSE (Data Science)\n\n"
                f"{d.get('description')}\n\n"
                f"**HOD:** {d.get('hod', {}).get('name')} (Email: {d.get('hod', {}).get('email')})\n\n"
                f"**Laboratories:**\n{labs}\n\n"
                f"**Key Focus:** Big data infrastructure, Apache Spark, predictive statistical modeling, and business intelligence.\n\n"
                f"**Source:** [Official SBJITMR Data Science]({d.get('url')})"
            ), sources

        if "mba department" in q or ("about" in q and "mba" in q):
            d = self.data.get("departments", {}).get("master_of_business_administration", {})
            sources.append({"title": "Official SBJITMR MBA Department", "url": d.get("url")})
            specs = ", ".join(d.get("specializations", []))
            return (
                f"### Department of Management Studies (MBA)\n\n"
                f"{d.get('description')}\n\n"
                f"**HOD:** {d.get('hod', {}).get('name')} (Email: {d.get('hod', {}).get('email')})\n\n"
                f"**Specializations Offered:** {specs}\n\n"
                f"**Intake:** 120 seats (2-Year Full Time Program)\n\n"
                f"**Source:** [Official SBJITMR MBA Department]({d.get('url')})"
            ), sources

        # Direct Second Year (DSY) / Lateral Entry / Diploma Admission
        if any(w in q for w in ["direct second year", "dsy", "lateral entry", "second year admission", "diploma admission"]) or ("diploma" in q and any(k in q for k in ["admission", "second year", "btech", "b.tech", "eligibility", "join", "degree"])):
            adm = self.data.get("admissions", {})
            dsy = adm.get("programs", {}).get("b_tech_direct_second_year", {})
            hl = adm.get("admission_helpline", {})
            sources.append({"title": "Official SBJITMR DSY Admissions", "url": "https://sbjit.edu.in/direct-second-year-admissions-dsy/"})
            sources.append({"title": "Official SBJITMR Admissions Guide", "url": "https://www.sbjit.edu.in/admission/"})
            return (
                f"### Direct Second Year B.Tech (Lateral Entry / DSY) Admissions at SBJITMR\n\n"
                f"**Yes**, diploma holders can take admission directly into the second year of B.Tech at S. B. Jain Institute of Technology, Management & Research (DTE Code: **4197**).\n\n"
                f"#### Eligibility Criteria:\n"
                f"- **Diploma Holders:** Passed minimum 3-year Diploma examination in Engineering and Technology from an AICTE-approved institution with at least **45% aggregate marks** (at least **40% marks** for backward class categories, Economically Weaker Section (EWS), and Persons with Disability candidates belonging to Maharashtra State).\n"
                f"- **B.Sc. Degree Holders:** Passed B.Sc. Degree from a UGC-recognized university with at least **45% marks** (40% for reserved categories of Maharashtra) and passed 10+2 Examination with Mathematics as a subject.\n\n"
                f"#### Admission Procedure:\n"
                f"- Admissions are conducted through the **Centralized Admission Process (CAP)** administered by the **State Common Entrance Test Cell, Maharashtra** (`cetcell.mahacet.org`).\n"
                f"- Institute-level seats and vacant seats after CAP rounds are filled as per State CET Cell guidelines.\n\n"
                f"#### Admission Helpline:\n"
                f"- **Incharge:** {hl.get('incharge', 'Dr. Yogesh Shinde')}\n"
                f"- **Contact:** {', '.join(hl.get('phone_numbers', [])[:2])}\n"
                f"- **WhatsApp:** {hl.get('whatsapp', '+91-8999300998')}\n"
                f"- **Email:** `{hl.get('email', 'admission@sbjit.edu.in')}`\n\n"
                f"**Source:** [Official SBJITMR Direct Second Year Admissions](https://sbjit.edu.in/direct-second-year-admissions-dsy/)"
            ), sources

        # Admission process & general admission queries
        if any(w in q for w in ["admission process", "how to take admission", "admission procedure", "eligibility for admission", "how to apply", "admission documents", "documents for admission", "take admission", "get admission", "admission criteria"]):
            adm = self.data.get("admissions", {})
            btech = adm.get("programs", {}).get("b_tech_first_year", {})
            hl = adm.get("admission_helpline", {})
            sources.append({"title": "Official SBJITMR Admissions Guide", "url": "https://www.sbjit.edu.in/admission/"})
            sources.append({"title": "Official SBJITMR Admission Helpline", "url": "https://www.sbjit.edu.in/admissionhelpline/"})
            ans = (
                f"### Admission Process at SBJITMR (DTE Code: 4197)\n\n"
                f"Admissions to S. B. Jain Institute of Technology, Management & Research are conducted through the **Centralized Admission Process (CAP)** administered by the **State Common Entrance Test Cell, Maharashtra** (`cetcell.mahacet.org`).\n\n"
                f"#### B.Tech Eligibility & Procedure:\n"
                f"- **Eligibility:** 10+2 / HSC with Physics and Mathematics as compulsory subjects, securing at least 45% marks (40% for reserved categories of Maharashtra).\n"
                f"- **Entrance Exam:** Valid non-zero score in **MHT-CET** or **JEE (Main) Paper I**.\n"
                f"- **Application Steps:**\n"
                f"  1. Register on the Maharashtra CET Cell CAP portal.\n"
                f"  2. Complete document verification at a designated Scrutiny Center (E-Scrutiny or Physical).\n"
                f"  3. Fill option forms choosing SBJITMR (Choice Code: **4197**).\n"
                f"  4. Report to the institute with original documents upon seat allotment.\n\n"
                f"#### Admission Helpline:\n"
                f"- **Incharge:** {hl.get('incharge')}\n"
                f"- **Helpline Contacts:** {', '.join(hl.get('phone_numbers', []))}\n"
                f"- **WhatsApp:** {hl.get('whatsapp')}\n"
                f"- **Email:** {hl.get('email')}\n\n"
                f"**Source:** [Official SBJITMR Admission Page](https://www.sbjit.edu.in/admission/)"
            )
            return ans, sources

        # Fees & NEFT
        if any(w in q for w in ["what are the fees", "fee structure", "fees", "how much is the fee", "tuition fee", "neft", "bank details"]):
            f = self.data.get("fees", {})
            btech = f.get("course_wise_fee_structure", {}).get("b_tech_engineering", {})
            cats = btech.get("category_wise_net_payable", {})
            neft = f.get("bank_neft_rtgs_details", {})
            sources.append({"title": "Official SBJITMR Fee Information", "url": "https://www.sbjit.edu.in/student-scholarship/"})
            sources.append({"title": "Official SBJITMR NEFT Details", "url": "https://www.sbjit.edu.in/neft-details/"})
            ans = (
                f"### Fee Structure & Bank Payment Details\n\n"
                f"The tuition and development fees at SBJITMR are regulated and approved annually by the **Fee Regulating Authority (FRA)**, Government of Maharashtra.\n\n"
                f"#### B.Tech Fee Structure (Approximate):\n"
                f"- **Open / General Category:** ~₹1,20,000 to ₹1,27,000 per year (Total ~₹5.08 Lakhs for 4 years).\n"
                f"- **OBC / EBC (Income < ₹8 Lakhs):** 50% Tuition Fee concession via MahaDBT (~₹65,000 - ₹70,000/year).\n"
                f"- **SC / ST Category:** 100% Tuition & Development Fee covered under GOI Scholarship.\n"
                f"- **VJNT / SBC / TFWS:** 100% Tuition Fee waived (~₹15,000 - ₹18,000 development fee payable).\n\n"
                f"#### MBA Fee Structure:\n"
                f"- Approx. ₹1,00,000 per year (~₹2.01 Lakhs total for 2 years for Open category).\n\n"
                f"#### Official Bank NEFT / RTGS Details:\n"
                f"- **Account Name:** {neft.get('account_name')}\n"
                f"- **Account Number:** `{neft.get('account_number')}`\n"
                f"- **IFSC Code:** `{neft.get('ifsc_code')}`\n"
                f"- **Bank & Branch:** {neft.get('bank_name')}, {neft.get('branch')}\n"
                f"- **Demand Draft:** In favor of \"S. B. Jain Institute of Technology, Management & Research\" payable at NAGPUR.\n"
                f"- **Payment Confirmation Contacts:** {', '.join(neft.get('confirmation_contact_numbers', []))}\n\n"
                f"**Source:** [Official SBJITMR NEFT Details](https://www.sbjit.edu.in/neft-details/)"
            )
            return ans, sources

        # Scholarships
        if any(w in q for w in ["scholarship", "scholarships", "freeship", "financial aid", "concession"]):
            sch = self.data.get("scholarships", {})
            schemes = sch.get("government_scholarship_schemes", [])
            sources.append({"title": "Official SBJITMR Scholarships", "url": "https://www.sbjit.edu.in/student-scholarship/"})
            
            items = []
            for s in schemes[:6]:
                items.append(f"- **{s.get('category')} ({s.get('scheme')}):** {s.get('benefit')} (Income Limit: {s.get('income_limit')})")
            
            ans = (
                f"### Scholarships Available at SBJITMR\n\n"
                f"SBJITMR students are eligible for all major Government of Maharashtra (MahaDBT) and Government of India scholarships:\n\n"
                f"{chr(10).join(items)}\n"
                f"- **Minority Scholarship (Jain, Muslim, Sikh, Christian, Buddhist):** ₹25,000/year (State / Central).\n"
                f"- **Dr. Panjabrao Deshmukh Hostel Allowance:** ₹30,000/year for children of marginal farmers / registered laborers.\n"
                f"- **Institutional Scholarship:** Sir Shantilal Badjate (SSB) Memorial Scholarship for meritorious and needy students.\n\n"
                f"**Where to apply:** [MahaDBT Portal](https://mahadbtmahait.gov.in)\n\n"
                f"**Scholarship Cell Helpline:** Mr. Nilesh Gaulkar (+91-9764508160 / info@sbjit.edu.in)\n\n"
                f"**Source:** [Official SBJITMR Scholarships Guide](https://www.sbjit.edu.in/student-scholarship/)"
            )
            return ans, sources

        # Exam results / timetable / exam process
        if any(w in q for w in ["exam process", "check results", "exam results", "where can i check results", "exam timetable", "where can i find exam timetable", "examination"]):
            ex = self.data.get("examinations", {})
            coe = ex.get("examination_cell", {}).get("controller_of_examinations", {})
            cgpa = ex.get("cgpa_to_percentage_conversion", {})
            links = ex.get("official_links_and_portals", {})
            sources.append({"title": "Official SBJITMR Exam Cell", "url": links.get("exam_cell_main")})
            sources.append({"title": "Official SBJITMR Exam Results Portal", "url": links.get("exam_results")})
            ans = (
                f"### Examination System & Results Portal\n\n"
                f"SBJITMR operates an **Autonomous Examination Cell** supervised by the Controller of Examinations.\n\n"
                f"- **Controller of Examinations (CoE):** {coe.get('name')} (Email: `{coe.get('email')}`)\n"
                f"- **Exam Structure:** Continuous Assessment Tests (CAT-I, CAT-II) + End Semester Examination (ESE).\n"
                f"- **Official Exam Results:** Published online at the [SBJITMR Exam Results Portal]({links.get('exam_results')}).\n"
                f"- **Exam Timetable:** Available at the [SBJITMR Exam Timetable Portal]({links.get('exam_timetable')}).\n"
                f"- **Revaluation & Open Day:** Students can inspect evaluated answer papers during 'Open Day' and apply for revaluation.\n"
                f"- **CGPA to Percentage Formula:** `{cgpa.get('formula')}` (or CGPA * 10).\n\n"
                f"**Source:** [Official SBJITMR Exam Cell]({links.get('exam_cell_main')})"
            )
            return ans, sources

        # Placements & Recruiters
        if any(w in q for w in ["placement", "placements", "recruiters", "highest package", "average package", "tpo", "who are the recruiters", "tell me about placements"]):
            plc = self.data.get("placements", {})
            stats = plc.get("placement_statistics", {})
            tpo = plc.get("training_and_placement_cell", {}).get("head_tpo", {})
            tpo_off = plc.get("training_and_placement_cell", {}).get("tpo_officer", {})
            recs = plc.get("top_recruiters", [])
            sources.append({"title": "Official SBJITMR Placements", "url": "https://www.sbjit.edu.in/placements/"})
            sources.append({"title": "Official SBJITMR Recruiters", "url": "https://www.sbjit.edu.in/recruiters/"})
            
            ans = (
                f"### Placements & Corporate Recruitment at SBJITMR\n\n"
                f"The Training & Placement Department (**Igniters**) shields talent and shapes futures through rigorous technical and soft-skill preparation.\n\n"
                f"#### Verified Placement Statistics:\n"
                f"- **Highest Package:** **{stats.get('highest_package')}**\n"
                f"- **Average Package:** **{stats.get('average_package')}**\n"
                f"- **Total Placements:** Over **3,500+ students** placed\n"
                f"- **Recruiting Companies:** Over **600+ companies** engaged\n\n"
                f"#### Major Recruiters:\n"
                f"- {', '.join(recs[:10])}, and more.\n\n"
                f"#### Training & Placement Leadership:\n"
                f"- **Head, Training & Placement:** {tpo.get('name')} (Contact: `{tpo.get('contact')}`, Email: `{tpo.get('email')}`)\n"
                f"- **TPO Officer:** {tpo_off.get('name')} (Email: `{tpo_off.get('email')}`)\n\n"
                f"**Source:** [Official SBJITMR Placements Page](https://www.sbjit.edu.in/placements/)"
            )
            return ans, sources

        # Library
        if "library" in q:
            fac = self.data.get("facilities", {})
            lib = fac.get("central_library", {})
            staff = lib.get("staff", [])
            sources.append({"title": "Official SBJITMR Central Library", "url": "https://www.sbjit.edu.in/s-b-jain-library/"})
            feats = "\n".join([f"- {f}" for f in lib.get("automation_and_features", [])])
            ans = (
                f"### S. B. Jain Central Library\n\n"
                f"{lib.get('description')}\n\n"
                f"#### Key Features & Facilities:\n"
                f"{feats}\n\n"
                f"#### Library Incharge:\n"
                f"- **Librarian:** {staff[0].get('name')} ({staff[0].get('qualification')})\n"
                f"- **Assistant Librarian:** {staff[1].get('name')} ({staff[1].get('qualification')})\n\n"
                f"**Source:** [Official SBJITMR Library](https://www.sbjit.edu.in/s-b-jain-library/)"
            )
            return ans, sources

        # Transportation / Bus
        if any(w in q for w in ["transport", "transportation", "bus", "buses", "is transport available"]):
            fac = self.data.get("facilities", {})
            t = fac.get("transportation", {})
            sources.append({"title": "Official SBJITMR Transportation", "url": "https://www.sbjit.edu.in/transportation/"})
            ans = (
                f"### Transportation Facilities\n\n"
                f"Yes, comprehensive bus transportation is available for students and faculty.\n\n"
                f"- **Fleet:** SBJITMR operates a fleet of **20 buses** covering all major locations across **Nagpur, Kamptee, and Saoner**.\n"
                f"- **Timings:** Buses arrive at the campus by **10:00 AM** and depart at **5:30 PM**.\n"
                f"- **Safety Features:** All buses strictly comply with RTO norms, fitted with **Electronic Speed Governors, GPRS live tracking systems, First Aid boxes, Fire Extinguishers, and Emergency Exit Doors**.\n"
                f"- **Emergency Support:** A dedicated emergency vehicle is stationed on campus 24 hours a day.\n"
                f"- **Public Transit:** MSRTC buses also ply regularly along Katol/Kalmeshwar road right up to the college gate.\n\n"
                f"**Source:** [Official SBJITMR Transportation Page](https://www.sbjit.edu.in/transportation/)"
            )
            return ans, sources

        # Student activities / NSS / NCC / Sports
        if "nss" in q:
            act = self.data.get("student_activities", {})
            nss = act.get("nss_national_service_scheme", {})
            sources.append({"title": "Official SBJITMR NSS Cell", "url": "https://www.sbjit.edu.in/national-service-scheme-cell-nss/"})
            acts = "\n".join([f"- {a}" for a in nss.get("major_activities", [])])
            return (
                f"### National Service Scheme (NSS) at SBJITMR\n\n"
                f"{nss.get('overview')}\n\n"
                f"#### Major Community Activities:\n"
                f"{acts}\n\n"
                f"**Source:** [Official SBJITMR NSS Cell](https://www.sbjit.edu.in/national-service-scheme-cell-nss/)"
            ), sources

        if "ncc" in q:
            act = self.data.get("student_activities", {})
            ncc = act.get("ncc_national_cadet_corps", {})
            sources.append({"title": "Official SBJITMR Student Affairs", "url": "https://www.sbjit.edu.in/student-affairs/"})
            return (
                f"### National Cadet Corps (NCC) at SBJITMR\n\n"
                f"{ncc.get('overview')}\n\n"
                f"Under the guidance of the Office of Dean Students Affairs, NCC activities foster military discipline, leadership character, and fitness among students.\n\n"
                f"**Source:** [Official SBJITMR Student Affairs](https://www.sbjit.edu.in/student-affairs/)"
            ), sources

        if "sports" in q:
            act = self.data.get("student_activities", {})
            sp = act.get("sports_cell", {})
            sources.append({"title": "Official SBJITMR Sports Cell", "url": "https://www.sbjit.edu.in/sports/"})
            acts = "\n".join([f"- {a}" for a in sp.get("activities", [])])
            return (
                f"### Sports Facilities & Sports Cell\n\n"
                f"**Coordinator:** {sp.get('coordinator')}\n\n"
                f"#### Facilities & Activities:\n"
                f"{acts}\n"
                f"- Full playground for cricket, football, basketball, and volleyball.\n"
                f"- Campus gymnasium and indoor sports arena (table tennis, chess, badminton).\n"
                f"- Sports incentive marks policy for university and state tournaments.\n\n"
                f"**Source:** [Official SBJITMR Sports Cell](https://www.sbjit.edu.in/sports/)"
            ), sources

        if any(w in q for w in ["student activities", "student life", "clubs"]):
            act = self.data.get("student_activities", {})
            clubs = act.get("technical_clubs_and_forums", [])
            sources.append({"title": "Official SBJITMR Student Affairs", "url": "https://www.sbjit.edu.in/student-affairs/"})
            club_list = "\n".join([f"- **{c.get('name')}**: {c.get('activities')}" for c in clubs])
            return (
                f"### Student Activities and Clubs at SBJITMR\n\n"
                f"Extracurricular life is organized under the Office of Dean Students Affairs (Dr. Yogesh P. Shinde):\n\n"
                f"#### Technical Clubs & Forums:\n"
                f"{club_list}\n\n"
                f"#### Annual Festivals:\n"
                f"- **Technotsav:** National level technical symposium (hackathons, robotics, coding).\n"
                f"- **Manthan:** Annual cultural fest celebrating music, drama, dance, and arts.\n"
                f"- **NSS & NCC:** Active community outreach and defense leadership programs.\n\n"
                f"**Source:** [Official SBJITMR Student Affairs](https://www.sbjit.edu.in/student-affairs/)"
            ), sources

        # Vision and Mission
        if "vision and mission" in q or re.search(r'\b(vision|mission)\b', q):
            c = self.data.get("college", {})
            v = c.get("vision", {}).get("statement")
            m = c.get("mission", {}).get("points", [])
            sources.append({"title": "Official SBJITMR Vision & Mission", "url": "https://www.sbjit.edu.in/vision-mision/"})
            m_list = "\n".join([f"{i+1}. {pt}" for i, pt in enumerate(m)])
            return (
                f"### Vision and Mission of SBJITMR\n\n"
                f"#### Vision:\n"
                f"> \"{v}\"\n\n"
                f"#### Mission:\n"
                f"{m_list}\n\n"
                f"**Source:** [Official SBJITMR Vision & Mission](https://www.sbjit.edu.in/vision-mision/)"
            ), sources

        # Established year / When was established
        if any(w in q for w in ["when was sbjitmr established", "established", "history", "establishment"]):
            c = self.data.get("college", {})
            est = c.get("establishment", {})
            sources.append({"title": "Official SBJITMR About Us", "url": "https://www.sbjit.edu.in/about-us/"})
            return (
                f"### Establishment of SBJITMR\n\n"
                f"S. B. Jain Institute of Technology, Management & Research (SBJITMR) was **established in the year 2008** by the **Sir Shantilal Badjate Charitable Trust**.\n\n"
                f"It is an Autonomous Institute affiliated with Rashtrasant Tukadoji Maharaj Nagpur University (RTMNU), approved by AICTE New Delhi and DTE Maharashtra (DTE Code: 4197), and accredited with an **'A' Grade by NAAC**.\n\n"
                f"**Source:** [Official SBJITMR About Us](https://www.sbjit.edu.in/about-us/)"
            ), sources

        # Location / Where is located / Address
        if any(w in q for w in ["where is sbjitmr located", "where is it located", "location", "address"]):
            c = self.data.get("college", {})
            loc = c.get("campus_and_infrastructure", {}).get("location")
            phone = c.get("official_contacts", {}).get("telephone")
            sources.append({"title": "Official SBJITMR Contact Us", "url": "https://www.sbjit.edu.in/contact-us/"})
            return (
                f"### Location & Address of SBJITMR\n\n"
                f"**Address:**\n"
                f"S. B. Jain Institute of Technology, Management & Research,\n"
                f"Near Jain International School, Yerla Village, Kalmeshwar Road,\n"
                f"Nagpur, Maharashtra - 441501, India.\n\n"
                f"**Telephone:** {phone}\n"
                f"**Campus:** 14+ acres lush green campus located along Kalmeshwar Road, Nagpur.\n\n"
                f"**Source:** [Official SBJITMR Contact Page](https://www.sbjit.edu.in/contact-us/)"
            ), sources

        # Contact number / Official email / Official website
        if any(w in q for w in ["contact number", "official email", "official website", "contact details", "phone number"]):
            c = self.data.get("college", {}).get("official_contacts", {})
            sources.append({"title": "Official SBJITMR Contact Us", "url": "https://www.sbjit.edu.in/contact-us/"})
            return (
                f"### Official Contact Details of SBJITMR\n\n"
                f"- **Official Website:** [{c.get('website')}]({c.get('website')})\n"
                f"- **General Enquiry Email:** `{c.get('general_enquiry_email')}`\n"
                f"- **Principal Email:** `{c.get('principal_email')}`\n"
                f"- **Admission Email:** `{c.get('admission_email')}`\n"
                f"- **Exam Cell Email:** `{c.get('exam_cell_email')}`\n"
                f"- **T&P Cell Email:** `{c.get('placement_email')}`\n"
                f"- **Telephone Numbers:** {c.get('telephone')}\n"
                f"- **Admission Helpline Numbers:** {c.get('admission_helpline')}\n\n"
                f"**Source:** [Official SBJITMR Contact Us](https://www.sbjit.edu.in/contact-us/)"
            ), sources

        # College Management / Governing Body
        if any(w in q for w in ["college management", "governing body", "who is in the governing body"]):
            com = self.data.get("committees", {}).get("governing_body", {})
            sources.append({"title": "Official SBJITMR Governing Body", "url": "https://www.sbjit.edu.in/governing-body/"})
            return (
                f"### SBJITMR College Management & Governing Body\n\n"
                f"The institute is managed by the **Sir Shantilal Badjate Charitable Trust** under the leadership of executive visionaries including Chief Executive Officer **Mr. Sanjeev Agrawal** and Principal **Prof. (Dr.) Sanjay L. Badjate**.\n\n"
                f"The **Governing Body** serves as the apex decision-making authority responsible for institutional governance, budget allocations, academic autonomy oversight, and policy execution.\n\n"
                f"**Source:** [Official SBJITMR Governing Body](https://www.sbjit.edu.in/governing-body/)"
            ), sources

        # Academic Council
        if any(w in q for w in ["academic council", "who is in the academic council"]):
            com = self.data.get("committees", {}).get("academic_council", {})
            comp = com.get("composition", [])
            sources.append({"title": "Official SBJITMR Academic Council", "url": "https://www.sbjit.edu.in/academic-council/"})
            items = "\n".join([f"{m.get('sr')}. **{m.get('name')}** - {m.get('category')}" for m in comp[:10]])
            return (
                f"### Academic Council of SBJITMR\n\n"
                f"**Chairman:** {com.get('chairman')}\n"
                f"**Member Secretary:** {com.get('member_secretary')}\n\n"
                f"The Academic Council consists of 21 distinguished members including RTMNU University Nominees, Educationalists from VNIT Nagpur, Industry Leaders, all Department HODs, and Deans:\n\n"
                f"{items}\n"
                f"...and other department heads.\n\n"
                f"**Source:** [Official SBJITMR Academic Council](https://www.sbjit.edu.in/academic-council/)"
            ), sources

        # Specific Faculty Search by Name across all departments
        fac_data = self.data.get("faculty", {})
        if fac_data and isinstance(fac_data, dict):
            for dept_key, f_list in fac_data.items():
                if not isinstance(f_list, list):
                    continue
                for f in f_list:
                    f_name = f.get("name", "")
                    f_clean = re.sub(r'[^a-zA-Z0-9\s]', '', f_name).lower().strip()
                    name_parts = [p for p in f_clean.split() if p not in ["dr", "prof", "mr", "mrs", "ms"]]
                    if not name_parts:
                        continue
                    first_last = f"{name_parts[0]} {name_parts[-1]}"
                    if f_clean in q_clean or first_last in q_clean or (len(name_parts) >= 2 and all(p in q_clean for p in [name_parts[0], name_parts[-1]])):
                        dept_name = f.get("department", dept_key.replace("_", " ").title())
                        src_url = f.get("source", "https://www.sbjit.edu.in/")
                        sources.append({"title": f"{dept_name} Faculty", "url": src_url})
                        ans = (
                            f"### Faculty Profile: {f.get('name')}\n\n"
                            f"- **Designation:** {f.get('designation')}\n"
                            f"- **Department:** {dept_name}\n"
                            f"- **Qualification:** {f.get('qualification')}\n"
                            f"- **Email:** `{f.get('email')}`\n\n"
                            f"**Source:** [{dept_name} Faculty Directory]({src_url})"
                        )
                        return _ret(ans, sources, is_auth=True)

        # Department Faculty Overview
        if any(w in q for w in ["department faculty", "who are the faculty", "faculty members", "faculty"]):
            fac = self.data.get("faculty", {})
            cse_fac = fac.get("computer_science_and_engineering", [])
            sources.append({"title": "Official SBJITMR Faculty Directory", "url": "https://www.sbjit.edu.in/computer-science-and-engineering/"})
            items = "\n".join([f"- **{f.get('name')}**: {f.get('designation')} ({f.get('qualification')}) | Email: `{f.get('email')}`" for f in cse_fac[:6]])
            return (
                f"### SBJITMR Faculty Members (Publicly Verified Official Roster)\n\n"
                f"SBJITMR has highly experienced professors and doctorates across engineering and management departments. Below is an excerpt of official CSE faculty members:\n\n"
                f"{items}\n\n"
                f"Each department maintains a dedicated faculty directory on their official department portal.\n\n"
                f"**Source:** [Official SBJITMR Faculty Directory](https://www.sbjit.edu.in/computer-science-and-engineering/)"
            ), sources

        # Campus facilities overall
        if "facilities" in q or "campus facilities" in q:
            sources.append({"title": "Official SBJITMR Facilities", "url": "https://www.sbjit.edu.in/contact-us/"})
            return (
                f"### Campus Facilities at SBJITMR\n\n"
                f"SBJITMR offers comprehensive, state-of-the-art campus infrastructure:\n\n"
                f"- **Central Library:** Computerized, Web OPAC, Book Bank for all students, NPTEL local streaming server, national & international e-journals.\n"
                f"- **Transportation:** Fleet of 20 college buses covering Nagpur, Kamptee, and Saoner, equipped with GPS and speed governors.\n"
                f"- **High-Tech Labs:** GPU-enabled AI/ML lab, VLSI lab, CNC machines, power systems lab.\n"
                f"- **Sports & Gym:** Full-sized grounds for cricket and football, basketball court, indoor games, and modern fitness gymnasium.\n"
                f"- **Power Backup:** Heavy-duty diesel generator (DG) power backup for uninterrupted learning.\n"
                f"- **Canteen:** Hygienic vegetarian cafeteria providing wholesome meals and refreshments.\n"
                f"- **Student Support:** Dedicated Psychological & Career Counselling Cell and Student Grievance Redressal Cell.\n\n"
                f"**Source:** [Official SBJITMR Campus Information](https://www.sbjit.edu.in/contact-us/)"
            ), sources

        # If no local match found
        return None, []
