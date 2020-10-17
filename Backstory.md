# Built with Love for My "Spouse"...
From 2017 - 2019, I trained for the Web Technologies category (formerly Web Design and Development) in the "international youth Olympics of skills", WorldSkills. 

Since I had no coding background, I had to work extra hard to catch up to my seniors and snag a spot in the school team. I've spent so much time training that my friends have jokingly called WorldSkills my "spouse" :)

# ... but only because I fell flat on my face
Competitors' work are marked on a web server that runs on a Linux, Apache, MySQL, PHP (LAMP) stack. The server is in the same local area network as competitors' workstations and can only be accessed via a domain name, which is unique to each competitor.

Websites that fail to work on the server will be graded poorly (if at all) even if they work on the competitor's local development environment. That happened to me during WorldSkills ASEAN 2018 - the sudden inclusion of remote deployment in my workflow threw me off because I didn't have a remote server to practise with.

Therefore, after WorldSkills Kazan 2019, I helped my coaches set up a submission server so that future batches of Nanyang Polytechnic competitors could practice with remote deployment as part of their workflow. `sshftp` was born to replicate the segregation behaviour that I couldn't configure on the network level (due to the school's restrictions).

> I am happy that my efforts have paid off! My juniors, Jeryl and Jordan, won Gold and Silver respectively at WorldSkills Singapore 2020 :D

# Not my first solution
At the various WorldSkills competitons I'd attended, I realised that I couldn't access folders beyond my own during my SSH and FTP sessions. I found out that this feature was named "chroot" and initially configured the host machine as such.

However, `chroot` prevented SSH from working correctly - users no longer have access to commands like `mysql`, `php`, and `node`. None of the tutorials online helped too (or maybe I was too stressed back then with submissions to be able to implement it properly). 

It was then I remembered the existence of Docker and came up with `sshftp`.

# Challenges
I had never done "systems administration" before, but with the help of numerous tutorials online - especially those from Digital Ocean - I set up Apache, `SSH`, and `FTP` easily on the host machine.

Ubuntu Desktop alse took care of the Linux installation process for me, which allowed me avoid grappling with partition management.

# Known issues
There's an issue with simplexml in the Alpine environment - I couldn't get it to work, even after installing the packages. One day I'll come back and fix it :)
