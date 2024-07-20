USER_AGENT = "AnixartApp/8.2.1-23121216 (Android 11; SDK 30; arm64-v8a;)"
HEADERS = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json; charset=UTF-8",
    }
API_URL = "https://api.anixart.tv"
ENDPOINTS = {
    "filter": f"{API_URL}/filter"
#   release: {
#     info: `${API_URL}/release`,
#     episode: `${API_URL}/episode`,
#   },
#   user: {
#     profile: `${API_URL}/profile`,
#     bookmark: `${API_URL}/profile/list/all`,
#     history: `${API_URL}/history`,
#     favorite: `${API_URL}/favorite/all`,
#   },
#   filter: `${API_URL}/filter`,
#   auth: `${API_URL}/auth/signIn`,
#   user: {
#     history: `${API_URL}/history`,
#     watching: `${API_URL}/profile/list/all/1`,
#     planned: `${API_URL}/profile/list/all/2`,
#     watched: `${API_URL}/profile/list/all/3`,
#     delayed: `${API_URL}/profile/list/all/4`,
#     abandoned: `${API_URL}/profile/list/all/5`,
#     favorite: `${API_URL}/favorite`,
#   },
#   search: `${API_URL}/search/releases`,
#   statistic: {
#     addHistory: `${API_URL}/history/add`,
#     markWatched: `${API_URL}/episode/watch`,
#   },
}