## Quickstart
```bash
git clone https://github.com/jessescodes/flash_card_cli
cd flash_card_cli
python3 main.py
```

## Flashcard After Action Review/ synopsis
**Core Focus:** Spaced Repetitions (SM-2 Algorithm), Doubly linked priority
queue, 'sqlite3' persistence, & Strict Type Safety / Null Defense.

This will be shorter than my text_based_rpg review. Really the only reason
I made this was to annotate something really significant I learned during
this projects.

Today is day 45 of my learning to code, so I'm still very new. However I feel
this will be a lesson I want to look down on in the future. As such I wanted
to document this. Frankly I make a project like this every day/ every other
day just for practice. The only reason I'm posting this is for the lesson.

1. What was the goal?
2. What happened?
3. What did I learn?
4. What could I reproduce to write better code?

## What was the goal?

The goal of this project was learning to use SQL, or in this instance SQLite3 on
python. I've never used a db before, and understood they were important in 
programming, so I wanted to do something where a db would be an important part
of the program.

Honestly while the SQL was what the project started as it ended up being a really
huge stepping stone in my development of typing. Another thing that I got just
before this was a linter. I've been using nvim to code since like day 2, but
I wasn't using a linter/ formatter. The day before starting this I got a linter,
and saw all the red squigglies/ yellow squigglies in my code. Of course I didn't 
like that, so this project really dove deep into typing and writing clean typed
code.

## What happened?

Truth be told I had no idea what I should do next so I googled "programming 
projects to help learn SQL". Google responded with a flashcard cli based program 
where I implemented the SM 2 algorithm (something like that), to sort a group
of flashcards for studying. That's about as much as I read before digging into
it, and building the thing.

I probably should have looked at that algorithm more before jumping in to understand
it better, as I'm sure you can see from the FlashCard class I track too many
attributes for each class, and I had no idea I would need to track a self.id at 
first for db purposes either, but that's just kinda how learning works. In that
it was effective.

After making the FlashCard class I had my big decision to make. How was I going
to use these timestamps to actually sort my data, and access this data. I had
played with making doubly linked lists in isolation, and honestly this felt like
the perfect implementation for that. Take the doubly linked list, and I could 
very easily insert things into the middle of the data structure based on the
timestamp attribute my FlashCard class was carrying. This is also when I realized
I had probably done something wrong because I was looking for examples of that
algorithm and kept finding a "priority" attribute, and I definitely did not have
that attribute. Only a timestamp, but we pushed on. My thoughts were this: "even
if I don't have priority my timestamp will be mutated in a way in which the
earliest timestamp should always have the highest priority. As such if I order
my queue by that it will work as intended". Just pop off the head, and insert based
on timestamp. After I pop off the head, I run the SM 2 algorithmic equation on in 
to get the next timestamp, and push it back on the queue with that new value. Even 
if this wasn't how it was "supposed" to work it works perfectly for the purposes
of this program.

Making the FlashNode and FlashQueue class is where I made my biggest mistake though, 
and is the entire reason why I'm making this a repo, and writing this AAR.

Remember how I just got a linter? Well turns out my brain is allergic to these 
red and yellow squigglies, and I do everything in my power to make them not exist.
Which honestly feels like good practice. After research it seems these basically
just tell me if all my types are returning what I say they should etc, so if I don't 
have squigglies that means all my code is safe, and there won't be any MONGO 
edge case failures I didn't even recognize at first, and I really like that.

So while making the FlashNode class when I was making self.next and self.prev I 
was trying to be all high speed and thought: "when I detached a node from it's 
current position, or want the GC to 'sweep it up' I will be assigning those values 
as None so i made them self.next: FlashNode | None to account for that". And thus 
began what turned into a whole ordeal. When initing the FlashQueue I also had it 
take FlashCard | None because once again I knew my head and tail wouldn't be an 
actual FlashCard class. So I wanted to primitively type them as FlashCard | None 
in recognition of that...

I want to stop for a second to really appreciate that. When I wrote those 3 lines 
I was honestly proud of myself. I was thinking ahead. I was trying to be pre-emptive
with how I was writing my code. What I had just done was create absolute nightmare
fuel for myself.

Why nightmare fuel you ask?

Though honestly if you're a dev I'm sure you know exactly what those None/ Nil/
Null assignments did.

I spent the next Goodness knows how many hours tracing my logic. Writing conditionals 
to ensure things like "current" were not None then asserting they weren't None.
ON LITERALLY EVERYTHING. A doubly linked list right now is barely something I can 
write admittedly I'm learning... So writing that while having 10 squigglies laughing
at me was not something I want to experience again.

That's just the beginning because inside my main file. My poor way too long main
file written to be menus and sub menus inside the CLI. Not only did I need to guard 
a user inputting something random and crashing the program. I also had to guard
against my MASSIVE MISTAKE. Every time I used anything related to my queue... Which 
I'll be honest is literally every ting. Because my queue is my engine behind what
gives the user cards, and keeps the cards sorted... I would have to always ensure 
and assert that card was not None... Because well... It could be right? Because 
I wanted to be slick...

## Lessons Learned.

A couple massive lessons I learned in this project. One is typing in general.
Typing is important. Typing makes your life a lot easier when it comes to debugging. 
Typing makes your code look much more professional, and I learned this on the 
project before this one (That I didn't post a repo) it wasn't anything crazy. 
However, I learned typing is an ultimate asset in protecting your code.

For instance it's very easy to manipulate your function returns into two types.
If it returns a dict you know your api call was successful, if it returns a string 
you know your API call failed. Then when you write that into your main file it's 
super easy to keep your program from crashing based on a typecheck of the return. 
Simple isinstance() dict or string and you know exactly how to proceed forward.

Caveat: I'm not saying that to you the reader. I'm sure you understand concepts 
like that. I'm going over things I've learned, and I'm just emphasising the
importance of typing, and why it's a lesson learned.

So yes, typing is very very important. And down to the smallest helper functions 
and methods inside what we write it's very important to understand what type of 
data it takes, and what kind of data we produce. Then use those results to 
manipulate the data for our benefit.

The even bigger lesson I learned... None is not the magic SINGLETON I thought it 
was. Before this I'll be honest I definitely overused None. It was a crutch in my 
coding. If I didn't want to think about something. If I didn't know explicitly
where I was going to be getting a value from when writing a class I would assign 
it to None Type. Because it was simple, easy to use. The pointer never went anywhere 
it felt like a rock... Which admittedly it is, in many cases.

However None has a dark side. None Type is an absolute virus that will propagate
into every corner of your software if you leave it "hanging around" in the 
"bottom" levels of your code. Of course it's not malicious, but I'll tell you what
it definitely feels malicious When you spend hours guarding against it.

So biggest... ABSOLUTE HUGEST TAKEAWAY FROM THIS PROJECT? Don't use a None Type 
unless its necessary. I understand None is a useful tool. It's great having that
one memory address location we can just point at like a beacon in the virtual
horizon. However, that beacon is not magic. If you can figure out a way to type
a variable without None, and there's no way it would need to be None. It is definitely
best practice to do exactly that. Don't use None as a crutch Jesse. Use it as a
tool that is very very useful, but can be very very detrimental if not used
correctly.

Honestly another mistake I made, was I honestly wish I would've used a graph 
structure similar to my text based RPG rather than the really long main I used here
if I would have built a graph structure with connections. Nothing long I could have
Just built my FRONT, BACK, MAIN_MENU and ADD into their own classes with connections
dicts attached. Then used those connections to navigate between the cards I could
have really diminished the complexity of my main file. Which I didn't really like
during this project.

However I also don't want to just be cornered into solving problems only one way
which is why I tried this method with this project. I learned that a graph system
definitely feels more efficient, and it makes the main file more cohesive.

2 more mistakes I found during testing and I ran my code through an LLM to see 
if there was anything I missed. Ultimately I'm self taught so I do need to ask
for help, especially in "post production" environments. I really really don't want 
to form bad habits. So I'll generally run my code through an LLM after it's done 
and ask what is wrong with it. However, I won't change my code. 

I don't want perfect, I want my mistakes. Below are the mistakes made:
When the menu option is CARD_BACK I failed to guard against user inputs outside
of 1-5. Which could lead to some whacky calculations in my priority queue. This
honestly seems like a more lazy mistake from me. I wrote that part w/o thinking 
and it just slipped through the cracks.

The next is an issue that if a user were to go back with a card selected then 
study a card again I would have popped a card off the queue, and never returned it.
In the future when working with an object I pop off a queue I'll need to be sure
that "All roads lead to it being pushed" back on if I want it back on the queue. 
That's an honest oversight I probably wouldn't have thought about until I was told.
Moving forward I'll be more cognizant of objects who's sole refcnt() live inside
the scope of that stack frame, and I recognize how "fragile" that object actually
is. IE as soon as the frame pops it gets GCed immediately.

Last is I was updating mutable values inside my queue as I was calling them, however,
I wasn't saving those changes to the database. What this ultimately translates
to is the database never actually changing. It kinda stays frozen in time no matter
how much I use the Flashcards. I can Add cards yes, but I would never get the 
benefits of the Algorithm attached to it.

I have a calculation run every time on the earlier mentioned card back. Which
explicitly mutates the card objects. Making an update db function in my db class,
and calling that method every time I actually mutate a card would be best practice.

Like I said I won't be making those changes in my code... Because I don't want to 
bury the most important part of these exercises. I could easily get a better app 
for flashcards right now... I'm not doing this to make the app itself, I'm learning 
from these mistakes. Thus they must be documented and acknowledged.

## What went well? What to continue in the future?

Honestly I was happy with this project overall. I liked my implementation of the 
doubly linked list in a priority queue. That felt useful. I also really liked 
my implementation of dunder overloads in my Queue class to get things like __len__ 
based on a length value i track in the queue. I honestly thought that was pretty
clever. Because a linked list at memory level doesn't have a __len__. Adding something 
like that was something I was proud of... The __contains__ logic I wrote was nice 
too, and I plan to add some small features to incorporate that. Like a search
for flashcard function. I'm not sure yet, but knowing if a card is in your queue
is a nice feature to have... Basically giving the convenience of a list's __len__ 
and dicts key __contains__ dunders just makes for a useful tool.

Also I personally like writing in a strict typing way. I personally really enjoy
having complete control of how my program acts, and understanding exactly what
is going in and out. Or if there are side effects, and I can't tell what exactly 
is going in, I can still control what is coming out. And frankly that seems like
it's more useful than what I even realize right now. So yea. I think I'll continue 
typing as strictly as I can, and strive to maintain a very high level of control 
over my program at all stages.

Thanks for reading. Jessescodes 
