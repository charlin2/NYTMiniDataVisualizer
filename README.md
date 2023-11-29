# NYT Mini Leaderboard Scraper
## Description
The NYT games web and mobile apps display statistics for the full-size cross words, however, there is a lack of fun stats for anything related to the mini other than the leaderboards.

This project serves to address this issue by pulling a user's mini data and displaying statistics related to the user's solves in relation to other users on their leaderboard.

## Use
In order to access a user's mini data, we need to have their NYT-S cookie (a long random string).  Getting the cookie can be done in two ways:
1. Input login email and password directly into this application.
    * The app will take care of getting the cookie from the login information.
    * Note that this method is quite finicky and **may lead to getting locked out of your account (due to "bot login").**
2. **Recommended method**: Extract the cookie from browser using dev tools.
    * Log in to NYT and use "Inspect" to bring up the console.
    * Input the following line to get your cookie: ```document.cookie.split('; ').find(r=>r.startsWith('NYT-S')).split('=')[1]```
        * Command courtesy of [Observable](https://observablehq.com/@observablehq/nyt-minis)
    * Copy and paste your cookie into the application.
    * My own testing has shown that this method will not get you locked out of your account (fingers crossed).
    * As with any other sensitive data, keep your cookie safe! Anyone can spoof your account if they have your cookie (this application does not store your login/cookie).
  
## Progress
As of 11/29/2023, the backend is built using Flask and hosted on [render.com](https://render.com/) using a free account.

The frontend is being built using React (most likely).

### To-do
- [x] API to fetch mini data
- [ ] Frontend to display stats
