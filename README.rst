About BeatBox
=============

BeatBox is a mobile application to help neighborhood watch groups in cities like Chicago share information about public safety incidents.  Users sign up as part of a beat_ and send alerts via SMS or mobile web.  A "beat leader" then receives the alert and can choose to forward it on to other users in the beat.

Shane Shifflett came up with the idea after reporting about muggings in `Chicago's Chinatown neighborhood <http://news.medill.northwestern.edu/chicago/news.aspx?id=162645>`_.  He found that even though there was a community that was tightly knit and concerned about neighborhood safety but, because of language barriers, was unwilling to notify police, or waited hours to find an English speaker before reporting the incident.  BeatBox lets neighbors share alerts in real time and saves documentation to show the police at beat meetings.

It was created over the course of one weekend at `The Media Consortium's Mobile Hackathon <http://mobilehackathon.eventbrite.com/>`_.

**Some important features and design principles**

- *Accessible technology*: We want lots of different communities including lots of different people to be able to use this with the technology they have.  Our initial prototype works through both SMS and mobile web.
- *Don't freak out!*: Too often neighborhood safety alerts create more gossip or fear instead of useful information or community.  This app prioritizes small chunks of useful information and generates data as a starting point for conversations with neighbors, police, politicians and other community stakeholders.  All alerts are moderated by a human to try use community judgment to decide which information is important to share in real time.

We used the Chicago Tribune Apps Team's excellent Hello Newsroom App 
(http://blog.apps.chicagotribune.com/2010/02/17/hello-newsroom-a-simple-geodjango-application/) 
as a starting point because it had beat geometries already set up.  

 
.. _beat:

In Chicago, the police organize themselves by beats. This is the smallest unit for feedback, collaboration and accountability between police and the community.
