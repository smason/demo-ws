# Getting WebSockets, Django, and uWSGI to play nicely together

This was started from the uWSGI article
about [Offloading Websockets and Server-Sent Events][uwsgisse].  Going
through the article trying to figure out how everything works in a
small example before integrating WebSockets into our real code.  I'd
tried, and failed, to just get everything working together naively so
thought it sensible to get a minimal example working.

The basic idea seems to be to separate out the Django web server from
the one that serves WebSockets.  WebSockets require some sort of state
to be kept per connection, which can take various forms but some sort
of "green thread"s are obviously nicer on the host system than forking
a new process per connection.
Python's [gevent](http://www.gevent.org/) package seems to be the
recommended approach for doing event based IO, i.e. cooperate
multithreading a la `node`.

One aspect of the approach is that it's possible to start the
WebSocket processing within the Django code before 'handing off to the
`gevent` code.  For example, I expect to use this to perform
authentication within the existing code base and pass appropriate user
identifiers across via `uwsgi.add_var()`.

uWSGI has lots of ways of performing routing, with the nicest approach
seeming to be to call `uwsgi.route()` at the appropriate moment in the
Django code and is documented at the bottom of the
above [article][uwsgisse].  Unfortunately this seems to crash the
current (2.0.14) version of uWSGI as some variables aren't
initialised.  I submitted [pull request #1473][issue1473] fixing this
and am waiting to hear whether it's accepted.  Until then you might
want to use my [fork of uWSGI][myuwsgi].

[myuwsgi]: https://github.com/smason/uwsgi
[uwsgisse]: http://uwsgi-docs.readthedocs.io/en/latest/articles/OffloadingWebsocketsAndSSE.html
[issue1473]: https://github.com/unbit/uwsgi/pull/1473
