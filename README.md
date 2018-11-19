# hanja-kanji-index
Experimental code for automatically building an index of the correspondence between hanja and kanji.

This is a fun coding project for me to assist in my studies of Japanese and maintanence of Korean 
skills.  The end goal here is to have functionality for getting a mapping between Hanja and Kanji,
as well as Korean words to and from Japanese words via the characeter mappings.  To start off, 
this project will just provide lexical information in both languages given a character or word.

Currently the project is using the Korean and Japanese Wiktionary pages for a couple of reasons. 
For one, Wiktionary is under Creative Commons so I won't have any restrictions on distributing this.
Second, Wiktionary pages contain some translation-information which can bootstrap some of the
mapping operations.


Python Dependencies:
* xml (ElementTree)
* bz2
* mwparserfromhell

