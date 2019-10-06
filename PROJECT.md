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

