from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment

# Create your views here.
def post_list(request):
    """Homepage - published posts, newest first."""
    posts = Post.objects.filter(published=True)
    context = {"posts": posts}
    return render(request, "blog/post_list.html", context)

def post_detail(request, slug):
    """
    Single post with comments and a comment submission form.

    comment.body is rendered with |safe in the template so that any HTML a commenter submits is executed by the browser as-is. This simulates a common real-world mistake - rendering unsanitised user input.

    Phase 0: XSS script in a comment fires in the browser (alert pops).
    Phase 1: Same behaviour, but the browser logs a CSP violation report.
    Phase 2+: The browser blocks the inline script entirely - no alert.
    """
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comments.filter(approved=True)
    error = None

    if request.method == "POST":
        author_name = request.POST.get("author_name", "").strip()
        body = request.POST.get("body", "").strip()
        if not author_name or not body:
            error = "Both name and comment are required."
        else:
            Comment.objects.create(post=post, author_name=author_name, body=body)
            return redirect("post_detail", slug=slug)

    context = {
        "post": post,
        "comments": comments,
        "error": error,
    }
    return render(request, "blog/post_detail.html", context)
