# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 14:26:53 2018

@author: SimantaSarkar
"""
#Bachelor of Science (B.S.)
                    j = experiences['jobs']
                    with sqlite3.connect("info.db") as con:
                        cur = con.cursor()
                        if len(j)!=0:
                            for i in j:
                                experiences_title=i["title"]
                                experiences_company=i["company"]
                                experiences_date_range=i["date_range"]
                                experiences_location=i["location"]
                                experiences_description=i["description"]
                                
                                #ekhane shob calculation er pore save hobe
                                
                                print(experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description)
                                cur.execute('''insert into candidate(name,phone,email,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description,company_name, company_size, company_type, company_description, company_industry, company_location, company_num_employees, company_specialties, company_website, company_year_founded) 
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (name,phone,email,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description,company_name, company_size, company_type, company_description, company_industry, company_location, company_num_employees, company_specialties, company_website, company_year_founded,))
                                #con.commit()
                                lst = [name,phone,email,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description,company_name, company_size, company_type, company_description, company_industry, company_location, company_num_employees, company_specialties, company_website, company_year_founded]
                                lsst.append(lst)
                                lst = []
                                
                                
                                
                                
                                
                                
                                
                                
                    j = experiences['jobs']
                    with sqlite3.connect("info.db") as con:
                        cur = con.cursor()
                        work_key = len(j)
                        total_org =len(j)
                        pos=[]
                        pos_count=0
                        tenure=[]
                        cmp_cnt=[]
                        if len(j)!=0:
                            total_it_pro=1
                            lst_cmp=''
                            for i in j:
                                experiences_title=i["title"]
                                if i["title"] not in pos:
                                    pos.append(i["title"])
                                    pos_count+=1
                                experiences_company=i["company"]
                                
                                if i["company"] not in cmp_cnt:
                                    cmp_cnt.append(i["company"])
                                experiences_date_range=i["date_range"]
                                #experiences_date_range=i["total_tenure"]
                                if cur_company == i["company"]:
                                    tenure_cur = ut.tenure(i['total_tenure'])
                                experiences_location=i["location"]
                                experiences_description=i["description"]
                                
                                if lst_cmp==i["company"]:
                                    total_it_pro+=1
                                else:
                                    lst_cmp=i["company"]
                                    tenure.append(ut.tenure(i['total_tenure']))
                                
                                print(experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description)
                                cur.execute('''insert into candidate(name,phone,email,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description,company_name, company_size, company_type, company_description, company_industry, company_location, company_num_employees, company_specialties, company_website, company_year_founded) 
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (name,phone,email,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description,company_name, company_size, company_type, company_description, company_industry, company_location, company_num_employees, company_specialties, company_website, company_year_founded,))
                                #con.commit()
                                lst = [name,phone,email,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description,company_name, company_size, company_type, company_description, company_industry, company_location, company_num_employees, company_specialties, company_website, company_year_founded]
                                lsst.append(lst)
                                lst = []
                                
                            total_tenure = sum(tenure)
                            within_pro_avg = (total_tenure/12)/pos_count
                            #org_cng_avg = (total_tenure/12)/len(cmp_cnt)
                            total_tenure_days = total_tenure*30
                            #if len(cmp_cnt) !=0:
                            #    event = 1
                            #else:
                                #event = 0
                            print("++++++++++++++++++++++++++++")
                            print(total_tenure,within_pro_avg,total_tenure_days)
                            print("++++++++++++++++++++++++++++")                               
                                
                                
                                
                                
                                
                                
                                
x="""
Bachelor of Architecture (BArch)
Bachelor of Design (BDes, or SDes in Indonesia)
Bachelor of Arts (BA, AB, BS, BSc, SB, ScB)
Bachelor of Applied Arts (BAA)
Bachelor of Applied Arts and Science (BAAS)
Bachelor of Engineering (BEng, BE, BSE, BESc, BSEng, BASc, BTech, BSc(Eng), AMIE,GradIETE)
Bachelor of Technology (B.Tech. or B.Tech.)
Bachelor of Engineering Technology (BSET)
Bachelor of Business Administration (BBA)
International Business Economics (BIBE)
Bachelor of Science in Business (BSBA)
Bachelor of Management Studies (BMS)
Bachelor of Administrative Studies
Bachelor of International Business Economics (BIBE)
Bachelor of Commerce (BCom, or BComm)
Bachelor of Business (BBus or BBus)
Bachelor of Management and Organizational Studies (BMOS)
Bachelor of Business Science (BBusSc)
Bachelor of Accountancy (B.Acy. or B.Acc. or B. Accty)
Bachelor of Comptrolling (B.Acc.Sci. or B.Compt.)
Bachelor of Economics (BEc, BEconSc; sometimes BA(Econ) or BSc(Econ))
Bachelor of Arts in Organizational Management (BAOM)
Bachelor of Computing (BComp)
Bachelor of Computer Science (BCompSc)
Bachelor of Science in Information Technology (BSc IT)
Bachelor of Computer Applications (BCA)
Bachelor of Applied Science in Information Technology (BAppSc(IT))
Bachelor of Business Information Systems (BBIS)
Intercalated Bachelor of Science (BSc)
Bachelor of Medical Science (BMedSci)
Bachelor of Medical Biology (BMedBiol)
Doctorate of Dental Surgery (DDS)
Bachelor of Science in Nursing (BN, BNSc, BScN, BSN, BNurs, BSN, BHSc.)
Bachelor of Science in Public Health (BSPH)
Bachelor of Health Science (BHS & BHSc)
Bachelor of Science in Human Biology (BSc)
Bachelor of Kinesiology (BKin, BSc(Kin), BHK)
Bachelor of Aviation (BAvn)
Bachelor of Divinity (BD or BDiv)
Bachelor of Theology (B.Th.; Th.B. or BTheol)
Bachelor of Religious Studies (BRS)
Bachelor of Religious Education (BRE)
Bachelor of Fine Arts (BFA)
Bachelor of Film and Television (BF&TV)
Bachelor of Integrated studies (BIS)
Bachelor of Journalism (BJ, BAJ, BSJ or BJourn)
Bachelor of Landscape Architecture (BLArch)
Bachelor of Liberal Arts (B.L.A.; occasionally A.L.B.)
Bachelor of General Studies (BGS, BSGS)
Bachelor of Applied Studies (BAS)
Bachelor of Liberal Studies
Bachelor of Professional Studies (BPS)
Bachelor of Library Science (B.L.S., B.Lib.)
Bachelor of Library and Information Science (B.L.I.S.)
Bachelor of Music (BM or BMus)
Bachelor of Art in Music (BA in Music)
Bachelor of Music Education (BME)
Bachelor of Mortuary Science (BMS)
Bachelor of Philosophy (BPhil, PhB)
Bachelor of Arts in Psychology (BAPSY)
Bachelor of Science in Psychology (BSc(Psych)
Bachelor of Science in Education (BSE, BS in Ed)
Bachelor of Science in Finance
Bachelor of Arts for Teaching (BAT)
Bachelor of Science and/with education degree (BScEd)
Bachelor of Science in Forestry (B.S.F. or B.Sc.F.)
Bachelor of Applied Science (BASc)
Bachelor of Science in Law (BSL)
Bachelor of Social Science (BSocSc)
Bachelor of Arts in Social Work (BSW or BASW)
Bachelor of Technology (B.Tech)
Bachelor of Talmudic Law (BTL)
Bachelor of Tourism Studies (BTS)
Bachelor of Mathematics (BMath)
Bachelor of Mathematical Sciences (BMathSc)
Bachelor of Urban and Regional Planning (BURP and BPlan)
Bachelor of Public Affairs and Policy Management (BPAPM)
"""

y="""
Master of Accountancy (MAcc, MAc, or MAcy)
Master of Advanced Study (M.A.S.)
Master of Economics (M.Econ)
Master of Applied Science (MASc, MAppSc, MApplSc, M.A.Sc. and MAS.)
Master of Architecture (M.Arch.)
Master of Arts (M.A., MA, A.M., or AM)
Master of Arts in Teaching (MAT)
Master of Arts in Liberal Studies (MA, ALM, MLA, MLS or MALS)
Master of Business Administration (MBA or M.B.A.)
Master of Business (MBus)
Master of Business Informatics (MBI)
Master of Chemistry (MChem)
Master of City Planning
Master of Commerce (MCom or MComm)
Master of Computational Finance (or Quantitative Finance)
Master of Computer Applications (MCA)
Master of Criminal Justice (MCJ)
Master in Creative Technologies
Master of Design (MDes, M.Des. or M.Design)
Master of Divinity (M.Div.)
Master of Economics (M.Econ.)
Master of Education (M.Ed., MEd, Ed.M., M.A.Ed., M.S.Ed., M.S.E., or M.Ed.L)
Master of Engineering (M.Eng., ME or MEng)
Master of Engineering Management (MEM)
Master of Enterprise (M.Ent.)
Master of European Law (LL.M. Eur)
Master of Finance (M.Fin.)
Master of Financial Economics
Master of Financial Engineering (Master of Quantitative Finance)
Master of Financial Mathematics (Master of Quantitative Finance)
Master of Fine Arts (MFA, M.F.A.)
Master of Health Administration (MHA)
Master of Health Science (MHS)
Master of Humanities (MH)
Master of Industrial and Labor Relations (MILR)
Master of International Affairs
Master of International Business
Masters in International Economics
Master of International Studies (MIS)
Master of Information System Management (abbreviated M.ISM, MS.IM, M.IS or similar)
Master of IT (abbreviated MSIT, MScIT, M.Sc.IT, MSc.IT or M.Sc IT.)
Master of Jurisprudence (M.J. or M.Jur)
Master of Laws (LL.M. or LLM)
Master of Studies in Law (M.S.L.)
Master of Landscape Architecture (M.Arch.)
Master of Letters (MLitt)
Master of Liberal Arts (MA, ALM, MLA, MLS or MALS)
Master of Library and Information Science (MLIS)
Master of Management (MM)
Master of Mathematical Finance
Master of Mathematics (or MMath)
Master of Medical Science
Master of Music (M.M. or M.Mus.)
Master of Occupational Therapy (OT)
Master of Pharmacy (MPharm or MPharm)
Master of Philosophy (M.Phil.)
Master of Physician Assistant Studies
Master of Physics (MPhys)
Master of Political Science
Master of Professional Studies (MPS or M.P.S.)
Master of Public Administration (MPA)
Master of Public Affairs (M.P.Aff.)
Master of Public Health (M.P.H.)
Master of Public Policy (M.P.P.)
Master of Public Management
Master of Quantitative Finance
Master of Rabbinic Studies (MRb)
Master of Real Estate Development
Master of Religious Education
Master of Research - MSc(R)
Master of Sacred Music (MSM)
Master of Sacred Theology (S.T.M.)
Master of Science (M.Sc., MSc, M.Sci., M.Si., Sc.M., M.S., MSHS, MS, Mag., Mg., Mgr, S.M., or SM)
Master of Science in Education
Master of Science in Engineering (MSE)
Master of Science in Finance (M.Fin.)
Master of Science in Human Resource Development (HRD or MSHRD)
Master of Science in Information Systems (MSIS)
Master of Science in Information Systems Management (MSMIS)
Master of Science in Information Technology (MSIT, MScIT, M.Sc.IT, MSc.IT or M.Sc IT.)
Master of Science in Leadership (MSL)
Master of Science in Management (MSc or MSM)
Master of Science in Nursing (MSN)
Master of Science in Project Management (M.S.P.M.)
Master of Science in Supply Chain Management (SCM or MSSCM)
Master of Science in Teaching (MST)
Master of Science in Taxation
Master of Social Science (MSSc)
Master of Social Work (MSW)
Master of Studies (M.St. or MSt)
Master of Surgery (Ch.M. or M.S., as well as M.Ch. and M.Chir.)
Master of Theological Studies (M.T.S.)
Master of Theology (Th.M. or M.Th.)
Master of Urban Planning
Master of Veterinary Science (MVSC or MVSc)"""

print(x.split())
     
