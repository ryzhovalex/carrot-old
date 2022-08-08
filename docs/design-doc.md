# Goals & Vision
Create todo list complying and extending personal experience on task management
and implementing best from Maxim Dorofeev's Jedi Techniques.

By building this application i'm solving these problems:
1. Minimalistic and simple todo app with only required functions. Available
   market todo apps have too many redundant functionality
2. There is only one app i know making some steps to implement Jedi Techniques:
   Singularity app. But, again, not everything suitable there (see problem #1)
3. No app implements my vision on task management, which i hope i can implement
   in my application

In terms of audience, i'm considering only myself, all new features will be
analyzed in first order through my experience, but i will appreciate adding
plugins for those who interested in adopting the application for themselves.

Product will be successful only if i will make usage of it on regular basis
for my personal projects and tasks.

# Requirements / System overview
## User requirements
1. As a user, i want to conveniently manage my tasks, projects and ideas, so
   that i can effectively manage Jedi's instances in one place
2. As a user, i want to have only required for me set of functionality, so
   that i can be more focused on completing my tasks, rather than playing
   with features.
3. As a user, i want to have access to core features / plugins that suits my
   needs, e.g. Jedi's `task ages`, so that i can implement my own vision to
   task management in the app

## Functional requirements
1. Minimal instance set: `Task`, `Project`, `Event`, `Idea`
2. Minimal functionality to operate with each instance of minimal instance set:
   CRUD, set dates (good reference of dynamic setting is Todoist [2]),
   reference each other, e.g. Add task to the Project, Convert an Idea to a
   Project/Task, Convert/Link an Event to a Project
3. Two-way synchronization with Google Calendar for instance `Event` and maybe
   for instances `Task` and `Project`
4. Two-way synchronization with telegram bot (for the first time Therminbot) to
   overview and modify app's instances
5. App should be hosted on web
6. App should have descriptive (OpenAPI) API specification
7. App should have functionality to implement and add own plugins
8. Main language: English. Other languages added by plugins
9. Projects can contain Tasks, Events and Ideas. Subprojects aren't allowed
10. Subtasks aren't allowed
11. Subevents aren't allowed
12. Subideas aren't allowed, only one description body per Idea
13. Task, Event or Idea could not have a parent Project directly
14. Unassigned to Project Tasks, Events or Ideas resides in meta-project called
    `Taskbox`

# References
1. [Design document structure example](https://blog.tara.ai/software-design-documents-template/)
2. [Todoist](https://todoist.com)
