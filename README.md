# Taligen

aka "Task List Generator"

There are many to-do-list apps, but they don't do well with repetitive
tasks that have to be performed exactly, or with slight variations,
one step after the other, tracking whether things worked out.

For example, imaging you need to repeatedly test a website, on three
different browsers and four different operating systems. Every time
the development team makes changes, you need to test again. And because
each browser and each OS is slightly different, there are some
variations to the exact steps to take.

This is what Taligen is for. You define a a text `.tlt` (Task List
Template) file, which defines what to do. For example, to test your
website on one OS with one browser, you might define a `onetest.tlt`
like this:

```
a: Start the browser $browser on your computer $computer
a: Go to http://example.com/
o: The site comes up
```

`a:` stands for an action, `o:` for an observation, and they will be
rendered accordingly with check boxes by `taliwodo` (but we get there
in a minute).

But you really need to test on the Mac, Windows and Linux, with Firefox,
Edge and Safari. So you create a master Task List Template called, for
example, `master.tlt`, like this:

```
call: onetest( browser=Firefox, computer=Mac )
call: onetest( browser=Safari, computer=Mac )
call: onetest( browser=Firefox, computer=Linux )
call: onetest( browser=Firefox, computer=Windows )
call: onetest( browser=Edge, computer=Windows )
```

When you run `taligen` on `master.tlt`, it will "include" `onetest.tlt`
once for each line that "calls" it, with the provided local parameters.
So the output is like this:

```
a: Start the browser Firefox on your computer Mac
a: Go to http://example.com/
o: The site comes up

a: Start the browser Safari on your computer Mac
a: Go to http://example.com/
o: The site comes up

a: Start the browser Firefox on your computer Linux
a: Go to http://example.com/
o: The site comes up

a: Start the browser Firefox on your computer Windows
a: Go to http://example.com/
o: The site comes up

a: Start the browser Edge on your computer Windows
a: Go to http://example.com/
o: The site comes up
```

Actually, we lied. The output is JSON, not that `.tlt` format. That
`.tlt` format only exists to make it really fast to create task lists.

What to do with the JSON? You pass it to `taliwodo`, the sibling web
application, which knows how to render it nicely. With checkboxes. So
you know exactly what you did and what not.

## Currently understood tags

`a: text` take action described by `text`

`o: text` make an observation described by `text`

`call: tlt( key=value key=value )` insert file `tlt` here and recursively
process it with the additional parameters in the parentheses. These parameters
are added to the parameters currently in effect

`set: key=value` set a parameter from the current position through the
rest of the `.tlt` file (and any `.tlt` files "called"` from it)

## Invocation

`taligen <file.tlt> <key=value> ... [ -o <out.json> | -O <outdir> ]`

This processes `<file.tlt>` and, recursively, all files "called" from it,
with the provided parameters given as `key=value`. Those may not be needed;
taligen will tell you. You can either generate a named JSON output file,
or get an auto-generated filename (that has the timestamp in it) in
a named directory (or, by default, the current directory).
