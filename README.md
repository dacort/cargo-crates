# Cargo Crates

An easy way to build data extractors in Docker.

Get it ... it's data containers ... cargo crates. 

Anyway.

## Usage

Convention over configuration(?).

Cargo crates share a common set of patterns that make them easy to use.

- Each crate is associated with a specific API.
- Authentication is provided via environment variables.
- Parameters are provided to the container at runtime.

For example, to extract sleep data from the Oura API you would run a container like this:

```shell
 docker run -e OURA_PAT=<TOKEN> ghcr.io/dacort/crates-oura
```

You can be more specific or select different APIs, too:

```shell
# Returns data beginning 2021-01-01
docker run -e OURA_PAT=<TOKEN> -e start=2021-01-01 ghcr.io/dacort/crates-oura
```

```shell
# Returns activity data instead of sleep data (the default)
docker run -e OURA_PAT=<TOKEN> ghcr.io/dacort/crates-oura activity
```

Other APIs might need more flexibility - for example, with Twitter there are numerous endpoints.

In this case, the `.env` file contains the environment variables needed for Twitter authentication.

```shell
# Extract current user info
docker run --env-file .env ghcr.io/dacort/crates-twitter users/show dacort

# Or fetch a user's followers
docker run --env-file .env ghcr.io/dacort/crates-twitter followers dacort
```

The idea is that the Docker container provides an abstraction on top of the underlying APIs and can be implemented however you want. 

Perhaps someday down the road there could be a set of base images that provide a nice set of abstractions for generic authentication and error handling. But for now, it's just a bunch of python.

## Caveats

Right now I'm building this for my own purposes. So the set of supported APIs or endpoints is rather limited.

## Supported Services

### GitHub

Supported Commands:
- `traffic` - returns results from GitHub traffic stats including clones, popular/paths, popular/referrers, and views. Each type of traffic stat is a subcommand.
- `releases` - returns information about releases for a specific GitHub repo.

Environment Variables:
- `GITHUB_PAT` - Your GitHub [Personal Access Token](https://github.com/settings/tokens)

Examples:
- Return all traffic stats for `dacort/cargo-crates`
    ```shell
    docker run -e GITHUB_PAT \
        ghcr.io/dacort/crates-github \
        traffic dacort/cargo-crates 
    ```
    ```json
    {"repo": "dacort/cargo-crates", "path": "clones", "stats": {"count": 77, "uniques": 8, "clones": [{"timestamp": "2021-03-18T00:00:00Z", "count": 77, "uniques": 8}]}}
    {"repo": "dacort/cargo-crates", "path": "popular/paths", "stats": [{"path": "/dacort/cargo-crates/actions", "title": "Actions \u00b7 dacort/cargo-crates", "count": 33, "uniques": 1}, {"path": "/dacort/cargo-crates", "title": "dacort/cargo-crates", "count": 11, "uniques": 2}, {"path": "/dacort/cargo-crates/actions/workflows/crates.yaml", "title": "Actions \u00b7 dacort/cargo-crates", "count": 7, "uniques": 1}, {"path": "/dacort/cargo-crates/actions/runs/666130915", "title": "Remove useless job0 \u00b7 dacort/cargo-crates@6b54337", "count": 4, "uniques": 1}, {"path": "/dacort/cargo-crates/actions/runs/666151009", "title": "Trying something else \u00b7 dacort/cargo-crates@ed3d226", "count": 3, "uniques": 1}, {"path": "/dacort/cargo-crates/actions/runs/666165537", "title": "Hmm \u00b7 dacort/cargo-crates@64c59e7", "count": 3, "uniques": 1}, {"path": "/dacort/cargo-crates/actions/runs/666215936", "title": "Add requirements \u00b7 dacort/cargo-crates@6161093", "count": 3, "uniques": 1}, {"path": "/dacort/cargo-crates/actions/runs/666227882", "title": "Does this actually work now?? \u00b7 dacort/cargo-crates@37d31ea", "count": 3, "uniques": 1}, {"path": "/dacort/cargo-crates/pulls", "title": "Pull requests \u00b7 dacort/cargo-crates", "count": 3, "uniques": 1}, {"path": "/dacort/cargo-crates/actions/workflows/test_matrix.yaml", "title": "Actions \u00b7 dacort/cargo-crates", "count": 2, "uniques": 1}]}
    {"repo": "dacort/cargo-crates", "path": "popular/referrers", "stats": [{"referrer": "github.com", "count": 3, "uniques": 2}]}
    {"repo": "dacort/cargo-crates", "path": "views", "stats": {"count": 108, "uniques": 2, "views": [{"timestamp": "2021-03-18T00:00:00Z", "count": 108, "uniques": 2}]}}
    ```
- Return only views for `dacort/cargo-crates`
    ```shell
    docker run -e GITHUB_PAT ghcr.io/dacort/crates-github traffic dacort/cargo-crates views
    ```
    ```json
    {"repo": "dacort/cargo-crates", "path": "views", "stats": {"count": 108, "uniques": 2, "views": [{"timestamp": "2021-03-18T00:00:00Z", "count": 108, "uniques": 2}]}}
    ```

### YouTube

Supported Commands:
- `videos` - return video stats for up to 50 video IDs.
- `channel_videos` - return video stats for 50 videos on the provided channel ID.

Environment Variables:
- `YOUTUBE_API_KEY` - An API key for the [YouTube Data API](https://developers.google.com/youtube/v3/docs)

Examples:
- Return video stats for [Intro to EMR Studio](https://www.youtube.com/watch?v=rZ3zeJ6WKPY)
    ```shell
    docker run -e YOUTUBE_API_KEY \
        ghcr.io/dacort/crates-youtube \
        videos rZ3zeJ6WKPY 
    ```
    <details>
        <summary>Click to view JSON</summary>
    ```json
    {
        "kind": "youtube#video",
        "etag": "tbhtHqbvEMe3jNGfFGK36HpowJk",
        "id": "rZ3zeJ6WKPY",
        "snippet": {
            "publishedAt": "2021-04-21T22:43:26Z",
            "channelId": "UCd6MoB9NC6uYN2grvUNT-Zg",
            "title": "Intro to Amazon EMR Studio",
            "description": "Introduction to Amazon EMR Studio. In this video, we show how to:\n- Create a new workspace\n- Utilize cluster templates for EMR clusters\n- Connect EMR Studio to a GitHub repository\n- Execute parameterized notebooks\n\nLearn more about Amazon EMR Studio - https://amzn.to/3xhbuEj\n\nSubscribe: \nMore AWS videos - http://bit.ly/2O3zS75 \nMore AWS events videos - http://bit.ly/316g9t4\n\n#AWS #AWSDemo #AmazonEMRStudio",
            "thumbnails": {
                "default": {
                    "url": "https://i.ytimg.com/vi/rZ3zeJ6WKPY/default.jpg",
                    "width": 120,
                    "height": 90
                },
                "medium": {
                    "url": "https://i.ytimg.com/vi/rZ3zeJ6WKPY/mqdefault.jpg",
                    "width": 320,
                    "height": 180
                },
                "high": {
                    "url": "https://i.ytimg.com/vi/rZ3zeJ6WKPY/hqdefault.jpg",
                    "width": 480,
                    "height": 360
                },
                "standard": {
                    "url": "https://i.ytimg.com/vi/rZ3zeJ6WKPY/sddefault.jpg",
                    "width": 640,
                    "height": 480
                },
                "maxres": {
                    "url": "https://i.ytimg.com/vi/rZ3zeJ6WKPY/maxresdefault.jpg",
                    "width": 1280,
                    "height": 720
                }
            },
            "channelTitle": "Amazon Web Services",
            "tags": [
                "AWS",
                "Amazon Web Services",
                "Cloud",
                "AWS Cloud",
                "Cloud Computing",
                "Amazon AWS",
                "Amazon EMR",
                "Amazon EMR Studio",
                "Jupyter"
            ],
            "categoryId": "28",
            "liveBroadcastContent": "none",
            "localized": {
                "title": "Intro to Amazon EMR Studio",
                "description": "Introduction to Amazon EMR Studio. In this video, we show how to:\n- Create a new workspace\n- Utilize cluster templates for EMR clusters\n- Connect EMR Studio to a GitHub repository\n- Execute parameterized notebooks\n\nLearn more about Amazon EMR Studio - https://amzn.to/3xhbuEj\n\nSubscribe: \nMore AWS videos - http://bit.ly/2O3zS75 \nMore AWS events videos - http://bit.ly/316g9t4\n\n#AWS #AWSDemo #AmazonEMRStudio"
            },
            "defaultAudioLanguage": "en"
        },
        "contentDetails": {
            "duration": "PT12M34S",
            "dimension": "2d",
            "definition": "hd",
            "caption": "false",
            "licensedContent": false,
            "contentRating": {},
            "projection": "rectangular"
        },
        "statistics": {
            "viewCount": "537",
            "likeCount": "9",
            "dislikeCount": "0",
            "favoriteCount": "0",
            "commentCount": "0"
        }
    }
    ```
    </details>

### Oura

Retrieve one of three different [daily summaries](https://cloud.ouraring.com/docs/daily-summaries) from the Oura Ring API.

Supported Commands:
- `sleep` - return [sleep periods](https://cloud.ouraring.com/docs/sleep)
- `activity` - return [activity summary](https://cloud.ouraring.com/docs/activity)
- `readiness` - return [readiness data](https://cloud.ouraring.com/docs/readiness)

Environment Variables:
- `OURA_PAT` - Your Oura [personal access token](https://cloud.ouraring.com/personal-access-tokens#)

Examples:
- Return sleep data for the past 7 days
    ```shell
    docker run -e OURA_PAT \
        ghcr.io/dacort/crates-oura \
        sleep | head -n 1
    ```
    <details>
        <summary>Click to view JSON</summary>
    ```json
    {
        "awake": 2010,
        "bedtime_end": "2021-04-20T06:55:43-07:00",
        "bedtime_end_delta": 24943,
        "bedtime_start": "2021-04-19T23:24:43-07:00",
        "bedtime_start_delta": -2117,
        "breath_average": 16.25,
        "deep": 4290,
        "duration": 27060,
        "efficiency": 93,
        "hr_5min": [
            63,
            63,
            64,
            65,
            66,
            66,
            66,
            67,
            66,
            66,
            67,
            70,
            71,
            70,
            69,
            69,
            70,
            69,
            68,
            68,
            68,
            67,
            67,
            66,
            66,
            66,
            66,
            66,
            62,
            64,
            70,
            68,
            67,
            66,
            66,
            67,
            66,
            66,
            65,
            66,
            66,
            67,
            67,
            67,
            67,
            70,
            69,
            71,
            71,
            69,
            68,
            66,
            63,
            65,
            67,
            66,
            65,
            64,
            63,
            62,
            63,
            65,
            66,
            65,
            69,
            72,
            74,
            72,
            68,
            68,
            69,
            68,
            66,
            62,
            63,
            62,
            61,
            60,
            60,
            58,
            60,
            57,
            58,
            57,
            57,
            58,
            61,
            64,
            66,
            61,
            0
        ],
        "hr_average": 65.68,
        "hr_lowest": 57,
        "hypnogram_5min": "4221111111222322221111222122223332222222223344333332222212222112333334233332222242222222444",
        "is_longest": 1,
        "light": 14730,
        "midpoint_at_delta": 11083,
        "midpoint_time": 13200,
        "onset_latency": 270,
        "period_id": 0,
        "rem": 6030,
        "restless": 29,
        "rmssd": 27,
        "rmssd_5min": [
            33,
            27,
            20,
            19,
            17,
            17,
            17,
            17,
            19,
            22,
            31,
            28,
            18,
            19,
            20,
            19,
            14,
            15,
            17,
            14,
            14,
            15,
            15,
            18,
            17,
            17,
            16,
            40,
            44,
            32,
            21,
            26,
            30,
            27,
            20,
            20,
            17,
            27,
            19,
            16,
            18,
            22,
            23,
            24,
            33,
            23,
            27,
            19,
            19,
            19,
            36,
            29,
            38,
            29,
            27,
            27,
            36,
            31,
            29,
            34,
            29,
            28,
            24,
            36,
            26,
            23,
            19,
            17,
            31,
            30,
            29,
            30,
            32,
            47,
            39,
            30,
            44,
            53,
            48,
            41,
            42,
            65,
            47,
            62,
            48,
            39,
            36,
            22,
            26,
            36,
            0
        ],
        "score": 83,
        "score_alignment": 97,
        "score_deep": 88,
        "score_disturbances": 77,
        "score_efficiency": 98,
        "score_latency": 72,
        "score_rem": 91,
        "score_total": 77,
        "summary_date": "2021-04-19",
        "temperature_delta": 0.06,
        "temperature_deviation": 0.06,
        "temperature_trend_deviation": 0.29,
        "timezone": -420,
        "total": 25050,
        "activity_type": "sleep"
    }
    ```
    </details>

### Reddit API

I wanted to get my saved posts out of the [Reddit API](https://www.reddit.com/dev/api). It's a little tough to understand, and the saved posts aren't actually documented there...but after [some hunting](https://www.reddit.com/r/redditdev/comments/91g3ek/api_403_while_trying_to_get_my_saved_posts/), I found that they can be accessed at `/user/dacort/saved.json`.

This functionality just fetches the most recent 100 saved posts every time. I considered adding a `start_date` filter, but don't need it right now. 😁

Supported Commands:
- saved <username> - list saved posts for `<username>`
- search [subreddit] <search_term> - search all of Reddit or a specific subreddit (`r/subreddit_name`) for a search term
    - Note that terms in quotes need to be surrounded in single quotes, e.g. `'"cargo crates"'`

Environment Variables:
- CLIENT_ID - Client ID of a ["script"](https://www.reddit.com/prefs/apps) type app
- CLIENT_SECRET - App secret
- USERNAME - Your Reddit username
- PASSWORD - Your Reddit password

### Slack Web API

The [Slack Web API](https://api.slack.com/web) is intended for use with ad-hoc queries and I use it to query basic info about some of the channels I'm in.

Supported Commands:
- `channels` - [list all channels](https://api.slack.com/methods/conversations.list) in a Slack team
- `search` - [search for a keyword](https://api.slack.com/methods/search.messages) in your Slack team

Environment Variables:
- `SLACK_TOKEN` - Some sort of Slack token that starts with `xox...`

Examples:

1. Get a list of channels for the workspace the token is associated with

```shell
docker run -e SLACK_TOKEN \
    ghcr.io/dacort/crates-slack channels
```

2. Perform a search in the workspace the token is associated with

```shell
docker run -e SLACK_TOKEN \
    ghcr.io/dacort/crates-slack search dacort
```

### Twitter

Only a couple Twitter endpoints are defined at this point.

Supported Commands:
- `followers` - return list of followers for a given screen name
- `users/show` - return user profile data for a given screen name

Environment Variables - create a Twitter app and define the 4 different variables.
- `CONSUMER_KEY`
- `CONSUMER_SECRET`
- `ACCESS_TOKEN_KEY`
- `ACCESS_TOKEN_SECRET`

You can store all these environment variables in a file and reference that file with Docker.

Examples:
- Return [@dacort's](https://twitter.com/dacort) profile
    ```shell
    docker run --env-file .env \
        ghcr.io/dacort/crates-twitter \
        users/show dacort
    ```
    ```json
    {"id": "99723", "name": "Damon Cortesi", "username": "dacort"}
    ```

## Writing output to Amazon S3

The original idea behind this repo was that I could run these containers and easily output the resulting data to templated paths on S3. 

So I built another tool, called [Forklift](https://github.com/dacort/forklift), that comes bundled with each Cargo Crate.

If you run the container normally, the output gets printed to stdout. However, if you provide a `FORKLIFT_URI` environment variable,
the data will get written to the S3 path provided. You can templatize parts of the path with JSON keys or a couple helper functions.

For example, the command below will upload my profile info to `s3://<BUCKET>/forklift/twitter/dt=2021-05-15/dacort.json`

```shell
docker run \
    -e FORKLIFT_URI='s3://<BUCKET>/forklift/twitter/dt={{ today }}/{{json "username"}}.json' \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    --env-file .env \
    ghcr.io/dacort/crates-twitter users/show dacort
```
 
Note that we passed AWS credentials as environment variables. You will either need to do that or run the container in AWS using [instance profiles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html). 

## Some higher level thoughts after a few implementations

- The data is intended to be streamed
    - Output is always a JSON stream
- Each implementation is intended to be completely independent
    - They're all Python...they could be anything else!
- Each implementation is intended to be as lightweight as possible
    - Don't force unnecessary requirements into a crate

## Next steps

- Formalize the executor API and base class
    - I want a way to be able to register commands, their parameters, and required environment variables
- Formalize the output API and stdout/S3 classes
    - Right now it's pretty hardcoded into the GitHub crate

## Maybe someday

- A generic "auth" command for crates

## Resources

- [Python project structure](https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6)
- [Minimal Docker containers for Python](https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3)
- (ended up not using, but) [IO Streams with Python](https://medium.com/dev-bits/ultimate-guide-for-working-with-i-o-streams-and-zip-archives-in-python-3-6f3cf96dca50)
- [For building matrix builds](https://stackoverflow.com/questions/59977364/github-actions-how-use-strategy-matrix-with-script)
