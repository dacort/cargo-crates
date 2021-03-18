# Cargo Crates

An easy way to build data extractors in Docker.

Get it ... it's data containers ... cargo crates. 

Anyway.

## Usage

Convention over configuration(?).

Cargo crates share a common set of patterns that make them easy to use.

- Each crate is associated with a specific API.
- Authentication is provide via environment variables.
- Parameters are provided to the container at runtime.

For example, to extract sleep data from the Oura API you would run a container like this:

```shell
 docker run --env-file .env cargo-crates/oura
```

You can be more specific or select different APIs, too:

```shell
# Returns data beginning 2021-01-01
docker run --env-file .env -e start=2021-01-01 cargo-crates/oura
```

```shell
# Returns activity data instead of sleep data (the default)
docker run --env-file .env cargo-crates/oura activity
```

Other APIs might need more flexibility - for example, with Twitter there are numerous endpoints:

```shell
# Extract current user info
docker run cargo-crates/twitter:v1 users/show

# Or fetch a specific tweet
docker run cargo-crates/twitter:v2 tweets/show/1234567890987654321
```

The idea is that the Docker container provides an abstraction on top of the underlying APIs and can be implemented however you want. 

Perhaps someday down the road there could be a set of base images that provide a nice set of abstractions for generic authentication and error handling. But for now, it's just a bunch of python.

## Some higher level thoughts after a few implmentations

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