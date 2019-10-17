
# Bid 

Continuous integration (CI) is identified as one of the primary practices to implement XP. According to Duvall et al., CI originated from the imperatives of agility, in order to respond to customer requests quickly. When building the source code, CI tools can execute unit and integration tests to ensure quality of the integrated source code. If the tests do not pass, CI tools can be customized to give feedback on the submitted code changes. Even though the concept of CI was introduced in 2006, initial usage of CI was not popular amongst practitioners. However, since 2011, with the advent of CI tools such as Travis CI, usage of CI has increased in recent years.

To implement CI, the team must maintain its source code in a version control system (VCS), and integrate the VCS with the CI tool so that builds are triggered upon submission of each commit. Programmers make commits in a repository maintained by a VCS such as, GitHub, and these commits trigger CI jobs on a CI tool such as Travis CI which executes, builds, tests, and produces build results. These build results are provided to the programmers as a feedback either through e-mails, or phone alerts on their submitted code changes. Based on the build results, programmers make necessary changes to their code, and repeats the CI process again.

When a software team adopts CI, the team has to follow a set of practices namely, submitting frequent commits, and submitting small-sized commits. However, in prior work researchers have observed that programmers don’t follow the best practices of CI such as submitting small-sized commits. Researcher have also suggested that not following the best practices of CI may not yield benefits in software development for example, quicker bug resolution. If CI best practices are not followed then there will be no observable influence of CI for bug resolution. 

Based on prior research, we hypothesize, implementing CI best practices is correlated with resolution security bugs in software. In a software project if a team doesn’t apply the best practices of CI, then security bug resolution will be affected i.e., we will not observe any quantifiable evidence before and after adoption of security bugs in software projects. 

We evaluate our hypothesis by mining 3,865 open source scientific software (OSSS) projects that use CI, and hosted on GitHub. Scientific software is defined as software that is used to explore and analyze data to investigate unanswered research questions in the scientific community. The domain of scientific software includes software needed to construct a research  pipeline such as software   for   simulation   and   data   analysis, large-scale dataset management,  communication  infrastructure,  and mathematical libraries. Programming languages such as Julia are used to develop scientific software efficiently and achieve desired program execution time. Julia was used in Celeste, a software used in astronomy research. Celeste was used to load 178 terabytes of astronomical image data to produce a catalog of 188 million astronomical objects in 14.6 minutes, yielding a program execution time improvement by a factor of 1,000, compared to prior implementation. 

We focus on scientific software projects because these projects have real-world implications for scientific research, finance-based institutions, and the energy sector. Unlike general purpose programming languages, we focus on Julia because Julia is a dedicated programming language for creating scientific applications. The above-mentioned Celeste-related example provides anecdotal evidence on the value of studying Julia-related projects for cybersecurity. Characterizing security bugs in real world Julia projects could help software developers in prioritizing verification and validation efforts, as well as identify if tools such as CI can actually help in reducing security bugs.    

We conduct our research project by mining bugs and security bugs that appear in our set of 3,865 repositories. We will apply qualitative analysis to construct a well-grounded security bug dataset. Next, we will mine two commit patterns namely, commit frequency and commit sizes from the collected 3,865 OSS repositories. We will quantify security bugs in the collected repositories. Next, we will use we introduce regression discontinuity design analyses to quantitatively evaluate the influence of CI on security bug resolution and commit patterns.  
