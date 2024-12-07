from os import environ
from typing import cast

from labhub import Directory, File, GitHubRepo, GitLabRepo


def create_gh_gl(ref: str = "main"):
    github_token = environ.get("GITHUB_TOKEN")
    assert github_token is not None

    gitlab_token = environ.get("GITLAB_TOKEN")
    assert gitlab_token is not None

    url = environ.get("GITLAB_HOST")
    if url is None:
        raise ValueError("$GITLAB_HOST is not defined")

    gh = GitHubRepo("hamolicious/test-repo", github_token, ref=ref)
    gl = GitLabRepo(53, gitlab_token, host=url, ref=ref)
    return gh, gl


gh, gl = create_gh_gl()


def test_ls_parity() -> None:
    files_gh = gh.ls()
    files_gl = gl.ls()

    fa = list(map(lambda f: f.name, files_gl))
    fb = list(map(lambda f: f.name, files_gh))
    assert fa == fb

    fa = list(map(lambda f: str(f.path), files_gl))
    fb = list(map(lambda f: str(f.path), files_gh))
    assert fa == fb


def test_ls_dir_parity() -> None:
    print()
    gh, gl = create_gh_gl(ref="dir-test")
    files_gh: list[Directory] = [f for f in gh.ls() if isinstance(f, Directory)]
    files_gl: list[Directory] = [f for f in gl.ls() if isinstance(f, Directory)]

    fa1 = list(map(lambda f: f.name, files_gl))
    fb1 = list(map(lambda f: f.name, files_gh))
    assert fa1 == fb1

    files_gh = gh.ls(cast(Directory, files_gh[0]).path)
    files_gl = gl.ls(cast(Directory, files_gl[0]).path)

    fa2 = list(map(lambda f: str(f.path), files_gl))
    fb2 = list(map(lambda f: str(f.path), files_gh))
    assert fa2 == fb2

    assert fa1 != fa2
    assert fb1 != fb2


def test_file_parity() -> None:
    files_gh: list[File] = [f for f in gh.ls() if isinstance(f, File)]
    files_gl: list[File] = [f for f in gl.ls() if isinstance(f, File)]

    fa = list(map(lambda f: f.get_data(), files_gl))
    fb = list(map(lambda f: f.get_data(), files_gh))

    assert fa == fb


def test_ref_parity() -> None:
    """
    Make sure that both retrieve the same files on a non-main branch
    and that they both retrieve the same files on the main branch

    finally, check that the files between the 2 branches are not the same (sanity check)
    """
    gl, gh = create_gh_gl(ref="other-branch")

    files_gh: list[File] = [f for f in gh.ls() if isinstance(f, File)]
    files_gl: list[File] = [f for f in gl.ls() if isinstance(f, File)]

    fa1 = list(map(lambda f: f.name, files_gl))
    fb1 = list(map(lambda f: f.name, files_gh))
    assert fa1 == fb1

    gl, gh = create_gh_gl(ref="main")

    files_gh = [f for f in gh.ls() if isinstance(f, File)]
    files_gl = [f for f in gl.ls() if isinstance(f, File)]

    fa2 = list(map(lambda f: f.name, files_gl))
    fb2 = list(map(lambda f: f.name, files_gh))
    assert fa1 == fb1

    assert fa1 != fa2
    assert fb1 != fb2
