"""Why the book exists.

Shared by the book's front matter and the website's about page, in the same way
kit and rollback_data are shared, so the two cannot drift apart. Edit it here and
both outputs follow.

Paragraphs carry `<b>` for emphasis and a `{repo}` slot each output fills for
itself: the printed book has nowhere to put a link, so it prints the address; the
website makes it clickable.
"""

KICKER = 'Why this book exists'

# Two lines, so print can break the heading where it wants and the web can let it
# wrap on its own.
HEADING_LINES = ['You are allowed to', 'run your own computers']

PARAS = [
    'A generation of engineers has now been trained to believe that owning a server is a '
    'kind of professional failure. It is not. It is a trade, and like every trade it has '
    'terms: you choose dedicated capacity, rented or owned in colocation, and keep '
    'more of the budget as your workload grows. Existing cloud ops engineers transition '
    'to on-premises platform work; contracted physical tasks go to remote hands, '
    'already priced in the facility bill, or to the rental provider. The model keeps '
    'the same hours and salary. On-premises roles can cost less than cloud specialist '
    'roles, but those potential savings are not counted. For a company with steady '
    'demand and a substantial cloud bill, '
    'both routes deserve a serious comparison.',

    'What has been missing is not the argument. It is a plan short enough to finish. '
    'Repatriation is written about as a decision and executed as a crisis, which is why '
    'so many attempts stall halfway, with two platforms live and nobody able to say '
    'whether it is going well. This is the other thing: {count} Moves, in five stages, '
    'each one a single job with an estimated cutover, a stated risk and explicit '
    'limits on reversal. An earlier edition of this book had a hundred and twenty-two of them and '
    'took four years. Nobody has four years.',

    'It is honest about the parts that do not pay. One whole Move ends by telling you to '
    'keep paying somebody else, because a content network, denial-of-service scrubbing '
    'and outbound email are three things you will not beat on your own, and a book that '
    'pretends otherwise is selling something. Another gives you permission to read three '
    'Moves, do the arithmetic, and stop. The point was never to own everything. It was '
    'to own the parts where ownership is cheaper, faster and yours.',

    'Which is why the whole thing is <b>open source</b>. Every Move, the typesetter that '
    'turns them into this book, and the site that publishes them are yours: the text '
    'under Creative Commons, the software under the MIT licence, all of it at {repo}. '
    'Correct it, extend it, add the services your own estate actually runs. '
    'Infrastructure knowledge this practical should not sit behind a consulting invoice.',
]


def paras(repo, count):
    """The paragraphs, with the repository address and the Move count filled in.

    The count is passed rather than written, so the prose cannot drift from the
    number of files in moves/ the way a hardcoded figure would.
    """
    return [p.replace('{repo}', repo).replace('{count}', str(count)) for p in PARAS]
