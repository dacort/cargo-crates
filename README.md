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

Examples:
- Return all traffic stats for `dacort/cargo-crates`
    ```shell
    docker run -e GITHUB_PAT ghcr.io/dacort/crates-github traffic dacort/cargo-crates 
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