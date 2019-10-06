# Quantifying Influence of Continuous Integration on Security Bug Resolution in Scientific Software Projects 

## Introduction 

Continuous integration (CI) originated from the imperatives of agility in order to respond to customer requests quickly. When building the source code, CI tools can execute unit and integration tests to ensure quality of the integrated source code. If the tests do not pass, CI tools can be customized to give feedback on the submitted code changes. Even though the concept of CI was introduced in 2006, initial usage of CI was not popular amongst practitioners. However, since 2011, with the advent of CI tools such as Travis CI, usage of CI has increased in recent years.

When a software team adopts CI, the team has to follow a set of practices. According to the CI methodology all programmers have to check-in their code daily, which are integrated daily. Unlike, traditional methodologies such as waterfall, in CI, programmers get instant feedback on their code via build results. To implement CI, the team must maintain its source code in a version control system (VCS), and integrate the VCS with the CI tool so that builds are triggered upon submission of each commit. Figure~\ref{figure-ci-bg} provides an example on how a typical CI process works. Programmer make commits in a repository maintained by a VCS such as, GitHub, and these commits trigger CI jobs on a CI tool such as Travis CI which executes, builds, tests, and produces build results. These build results are provided to the programmers as a feedback either through e-mails, or phone alerts on their submitted code changes. Based on the build results, programmers make necessary changes to their code, and repeats the CI process again.

Prior research has observed CI to have a beneficial impact on software quality and productivity. By taking motivation from prior research, we hypothesize that CI will help in resolving security bugs for developers. We evaluate our hypothesis by mining open source scientific software (OSSS) projects that use CI, and hosted on GitHub. 

Scientific software is defined as software that is used to explore and analyze data to investigate unanswered research questions in the scientific community~\cite{hawker:software:science}. The domain of scientific software includes software needed to construct a research  pipeline such as software   for   simulation   and   data   analysis, large-scale dataset management,  communication  infrastructure,  and mathematical libraries~\cite{carver:software:science}~\cite{paigemsr2019}. Programming languages such as Julia are used to develop scientific software efficiently and achieve desired program execution time. Julia was used in [Celeste](https://www.hpcwire.com/off-the-wire/julia-joins-petaflop-club/), a software used in astronomy research. Celeste was used to load 178 terabytes of astronomical image data to produce a catalog of 188 million astronomical objects in 14.6 minutes, yielding a program execution time improvement by a factor of 1,000, compared to prior [implementation](https://juliacomputing.com/case-studies/celeste.html). The Celeste-related example provides an anecdotal evidence on how Julia could be beneficial to achieve desired program execution time, and complete computations tasks efficiently.  

%When a software team adopts CI, the team has to follow a set of practices namely, submitting frequent commits, and submitting small-sized commits. However, in prior work researchers have observed that programmers don't follow the best practices of CI such as submitting small-sized commits. 

We focus on scientific software projects because these projects have real-world implications for scientific research, finance-based institutions, and the energy sector. Unlike general purpose programming languages, we focus on Julia because Julia is a dedicated programming language for creating scientific applications. The above-mentioned Celeste-related example provides anecdotal evidence on the value of studying Julia-related projects for cybersecurity. Characterizing security bugs in real world Julia projects could help software developers in prioritizing verification and validation efforts, as well as identify if tools such as CI can actually help in reducing security bugs.    

We will answer the following research questions: 

    -RQ1: How does continuous integration influence commit practices in open source scientific software projects?
    -RQ2: How does continuous integration influence resolution of bugs in open source scientific software projects?
    -RQ3: How does continuous integration influence resolution of security bugs in open source scientific software projects?

We conduct our research project by mining security bugs that appear in our set of OSSS repositories. We will apply qualitative analysis to construct a well-grounded security bug dataset. Next, we will mine two commit patterns namely, commit frequency and commit sizes from the collected OSSS repositories. We will quantify security bugs in the collected repositories. Next, we will use we introduce regression discontinuity design analyses to quantitatively evaluate the influence of CI on security bug resolution and commit patterns.  

## Specific Aims

The specific aims of our project is listed below: 

    -Repository gathering: We will perform large-scale data analysis by collecting repositories from GitHub, a social coding platform.
    -Construct dataset: We will use pattern matching and manual verification to identify security bugs reported in collected repositories. 
    -Quantify influence: We will use regression discontinuity design (RDD) to assess the influence of CI on security bug resolution. Along with RDD, we will also apply change point analysis~\cite{taylor2000change} to observe at what particular value does certain patterns change. We will also study statistics of commit patterns, and apply RDD to observe if CI infleunces commit patterns of developers.     

    Each task and corresponding deadline is listed in Table~\ref{table-timeline}. Details on each task is listed below: 

    -Task-Bid submission: We will bid for our proposed project by briefly describing our plans.
    -Task-Repository mining: We will use Google Big Query to collect repositories that are developed in the Julia programming language. We will use repository signals to filter out irrelevant repositories.  
    -Task-Grounded security bug dataset construction: We will use pattern matching as well as manual verification to identify which commits are related to security bugs. 
    -Task-Commit pattern mining: We will mine commit size and commit frequency patterns before and after adoption of CI. 
    -Task-Proposal submission: We will submit a document that lays out our proposed research methodology and preliminary results.  
    -Task-Regression analyses: We will use RDD to quantify if adoption of CI impacts security bug resolution and commit patterns. 
    -Task-Progress Report: We will report our progress so far as a document. 
    -Task-Final Report: We will submit the findings from our research study with appropriate sections namely, introduction, methodology, and threats to validity. 
    -Task-Final Presentation: The team members will present findings formally in front of other InSure participants

For each task we provide the status below: 

| Tasks                                      | Deadline     | Assignee                             | Status    |   |
|--------------------------------------------|--------------|--------------------------------------|-----------|---|
| Bid submission                             | Sep 16, 2019 | Justin Murphy                        | Completed |   |
| Repository mining                          | Sep 20, 2019 | Justin Murphy                        | Completed |   |
| Grounded security bug dataset construction | Sep 27, 2019 | Elyas Brady   and Kaitlyn Cottrell   | Completed |   |
| Commit pattern mining                      | Oct 04, 2019 | Justin Murphy and Kaitlyn Cottrell   | Completed |   |
| Proposal submission                        | Oct 04, 2019 | Justin Murphy                        | Completed |   |
| Regression Analyeses                       | Oct 25, 2019 | Elyas Brady                          | Completed |   |
| Final Report Submission                    | Dec 06, 2019 | J. Murphy, K. Cottrell, and E. Brady | Completed |   |

## Technical Approach

Working with longitudinal data rather than randomized observations for our research project, we will be implementing the quasi-experimental method of RDD analyses to quantitatively evaluate the influence of CI on security bug resolution and commit patterns. RDD is often applied with time-series data and can be used to model the magnitude of a discontinuity among the values of a function just before and after a particular intervention. RDD is considered as one of the more robust quasi-experimental designs, and is based on the assumption that in the absence of an intervention, the function would continue displaying the same trend as displayed prior to that intervention. Considering this assumption, it is possible to gauge how much of an effect an intervention has on the data not only at the time of the intervention, but over time as well. In our case the intervention will be the adoption of CI, specifically Travis CI. Along with RDD we will be incorporating multiple regression to assess any influence that may have come from variables other than the intervention, such as the number of developers on a project or age of the project at the time of intervention.

The two most common implementations of RDD are sharp RDD and fuzzy RDD, and for our project we will be using sharp RDD. To demonstrate this RDD method, some synthetic data was generated and used to illustrate a discontinuity.

## Team 

*Elias Brady*: Elias Brady is a Tennessee Ned Mcwherter Scholarship Recipient. He has been on the Dean's list each semester since he started at Tennessee Tech University, and currently maintains an institution wide GPA of 3.91 and a departmental GPA of 4.0. He has worked as a teacher's assistant for the UNIX-like systems lab as well. He is majoring in Computer Science because he loves to solve problems. Upon completion of his graduate studies, Elias is planning to work in industry for a year, go back to school for a Master's degree in robotics, and eventually become a doctorate in artificial intelligence.
 
*Kaitlyn Cottrell*: Kaitlyn Cottrell is currently a Computer Science major with a concentration in Cybersecurity at Tennessee Tech University. She has a 3.86 institution wide GPA. She is a mentor-in-training for the Defense Cyber Interest group and works on the CyberPatriot outreach with local middle schools done by the group, after participating in the competition for two years in high school. She has also worked as a counselor at the GenCyber camp at Tennessee Tech in Summer 2019. 

*Justin Murphy*: Justin Murphy is a senior fast-track student at Tennessee Tech University majoring in Computer Science concentrating in Cybersecurity.  He is actively involved with CEROC at Tennessee Tech and serves as the lead for the Capture the Flag (CTF) Cyber Interest Group.  He is a CyberCorps: SFS Scholar and intends to start pursuing his PhD degree in Computer Science at Tennessee Tech starting Fall '20.  He holds a previous undergraduate degree in Statistics from the University of Tennessee Knoxville (2011), and used to be a high school mathematics teacher in Nashville, Tennessee. 

*Akond Rahman* (Mentor): Akond Rahman is an Assistant Professor at Tennessee Tech University. Akond has extensive experience in mining large scale open source repositories, and have used mined data for software quality analysis and vulnerability analysis. Akond's recent research related to mining software repositories and cybersecurity was recognized by ACM in 2019, and awarded the ACM SIGSOFT Distinguished Paper at ICSE, which is ranked the most prestigious venue for software engineering research.  