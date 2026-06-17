# Curated exemplars for the production cognitive reframing pipeline.

CLASSIFIER_LABEL_TO_EXEMPLAR_KEY = {
    "Black-and-white or polarized thinking / All or nothing thinking": "all-or-nothing thinking",
    "Catastrophizing": "catastrophizing",
    "Discounting the positive": "disqualifying the positive",
    "Jumping to conclusions: Fortune-telling": "fortune telling",
    "Jumping to conclusions: mind reading": "mind reading",
    "Labeling and mislabeling": "labeling",
    "Mental filtering": "mental filtering",
    "Overgeneralization": "overgeneralizing",
    "Personalization": "personalizing",
    "Should statements": "should statements",
}

DEPLOYMENT_EXEMPLARS = {
    "all-or-nothing thinking": [
        {
            "situation": "I have been sketching every evening this week and most of the drawings haven't turned out the way I wanted",
            "thought": "If my drawings don't come out perfectly, I throw them in the trash.",
            "reframe": "Not every drawing has to come out perfectly. Each attempt is part of how I improve, and the ones I'm less happy with still teach me something."
        },
        {
            "situation": "I wasn't picked to play in the next soccer game with my team.",
            "thought": "My soccer days are over.",
            "reframe": "I wasn't picked to play in the next soccer game, but there will be soccer games in the future."
        },
        {
            "situation": "The hotel in Florida I usually book is all sold out.",
            "thought": "It's not even worth going at all now.",
            "reframe": "The hotel in Florida I usually book is all sold out. I will try to book another hotel. There are a lot to choice from.",
        }
    ],
    "catastrophizing": [
        {
            "situation": "Yesterday my kid was sick with the flu.",
            "thought": "I have the feeling he will end up in the hospital because of it",
            "reframe": "My kid is sick with the flu but he will get better soon."
        },
        {
            "situation": "I'm a teacher and I forgot to grade papers this week.",
            "thought": "I will forever lose the trust of my school.",
            "reframe": "I forgot to grade papers first time this week. This has happened to almost every teacher before, I'm sure the school will understand.",
        },
        {
            "situation": "My older sister hasn't called me for awhile.",
            "thought": "I am sure that she hates me, and she never wants to talk to me again.",
            "reframe": "I'm sure my sister is busy with her new kid, I will have to call her and see if everything is ok.",
        }
    ],
    "disqualifying the positive": [
        {
            "situation": "My favorite soccer team made it to the World Cup, but their best player got injured.",
            "thought": "It was all for nothing since the best player is injured.",
            "reframe": "My favorite soccer team made it to the world cup and their best player got injured but reaching the World Cup is still a great success."
        },
        {
            "situation": "My date told me she had a great time at the Kings of Leon concert last week.",
            "thought": "She has a great time only because of the band and I think she would have had a good time whether I was there or not.",
            "reframe": "My date had a great time at the Kinds of Leon concert last week with me so hopefully she will like the next date I plan as well",
        },
        {
            "situation": "I found a part-time job.",
            "thought": "Now I have a part-time job, but I'm ashamed that I don't have something more befitting my skillset and that pays more.",
            "reframe": "I have a part time job right now, but I will work hard towards having something that pays better and is more fulfilling.",
        }
    ],
    "fortune telling": [
        {
            "situation": "I don't go out often, but I did today and it was uncomfortable.",
            "thought": "I don't know how to socialize with people. I will be lonely my whole life.",
            "reframe": "I don't know how to socialize with people because I don't go out often, but I will work on getting better by going out more."
        },
        {
            "situation": "I ate pizza again yesterday.",
            "thought": "Since I like to eat pizza a lot, I'll never lose weight and be healthy.",
            "reframe": "Since I like to eat pizza a lot, I will schedule a cheat day each week to eat my favorite food, and follow a good diet the rest of the week.",
        },
        {
            "situation": "I have a school dance soon. I'd like to ask Suzy to the dance.",
            "thought": "I can not ask her because she'd turn me down.",
            "reframe": "I'd like to ask Suzy to the dance. I don't know if she'll accept, but even if she doesn't, I can ask another friend.",
        }
    ],
    "mind reading": [
        {
            "situation": "My neighbor calls me by my first name instead of my nickname.",
            "thought": "He probably thinks bubblegum is a tacky nickname.",
            "reframe": "My neighbor calls me by my first name instead of my nickname because he may think he doesn't know me well enough to use it. I will let him know that I don't mind if he calls me Bubblegum."
        },
        {
            "situation": "The sax player at the club last night kept looking at me.",
            "thought": "He must think I know nothing about jazz",
            "reframe": "The sax player at the club kept looking at me because he may have thought I looked cool.",
        },
        {
            "situation": "My parents are ignoring me.",
            "thought": "I am sure it's because they hate me for not driving them to the church.",
            "reframe": "My parents are ignoring me. I'm sure it is in my head and I will ask them if anything is wrong.",
        }
    ],
    "labeling": [
        {
            "situation": "I broke my nose when I was 10.",
            "thought": "I broke my nose because I wasn't a smart kid.",
            "reframe": "I broke my nose when I was 10. No matter how careful, many kids get a broken bone or stitches growing up."
        },
        {
            "situation": "I messed up the lines on my paper.",
            "thought": "I can't ever seem to draw anything right and am a worthless person.",
            "reframe": "Today is rough since I messed up my lines, I will just redo it until I get it right, which I will.",
        },
        {
            "situation": "I am in my last year of grad school and didn't earn enough credits to pass one of my classes.",
            "thought": "I'm a failure of a student.",
            "reframe": "I am in my last year of grad school and I am still a few credits short of one of my classes. I will ace all of my projects and exams in order to get the best grade possible.",
        }
    ],
    "mental filtering": [
        {
            "situation": "I have to pay the taxes today.",
            "thought": "I make a million dollars a year, but I have to pay so much in taxes.",
            "reframe": "I make a million dollars a year. Even after a taxes, I still have more than enough money leftover."
        },
        {
            "situation": "I enjoyed reading a history book today. The ending was bad.",
            "thought": "The ending ruined everything for me.",
            "reframe": "I enjoyed reading a history book today even if I didn't like the ending.",
        },
        {
            "situation": "I bought a new guitar. It sounds amazing, but they did not have it in blue color.",
            "thought": "I hate my new guitar, it isn't blue, so I don't want it.",
            "reframe": "My new guitar sounds amazing and is worth a lot of money. It isn't my favorite color but I can appreciate the other redeeming qualities about it and enjoy it.",
        }
    ],
    "overgeneralizing": [
        {
            "situation": "I did not turn off the lights at night.",
            "thought": "Now I will never achieve my goal of a green planet.",
            "reframe": "While I'm an environmentalist and I didn't turn off my lights last night, many other people make this same mistake."
        },
        {
            "situation": "I am bad at playing electric violin.",
            "thought": "I'll never be able to play any music instrument",
            "reframe": "I am bad at playing electric violin. I'm going to try a different instrument, which I might be better at.",
        },
        {
            "situation": "My husband and I are planning a trip when he retires. We cannot agree on a hotel.",
            "thought": "The whole trip will be disappointing.",
            "reframe": "If we really cannot agree on a hotel, we should just flip a coin and not argue about it.",
        }
    ],
    "personalizing": [
        {
            "situation": "I never eat veggies because I throw up every time I try.",
            "thought": "I will never achieve my goal now of a green planet.",
            "reframe": "While I'm an environmentalist and I didn't turn off my lights last night, many other people make this same mistake."
        },
        {
            "situation": "Three people quit their jobs the week after I brought donuts to the office.",
            "thought": "My job was going great, but one day I brought donuts and three people quit.",
            "reframe": "I'm sure it was a coincidence and not due to the donuts. However, I could find out why they left.",
        },
        {
            "situation": "The other day one of my other employees was blamed for the stuff on the shelf falling.",
            "thought": "It's because I usually stock shelves and I am irresponsible.",
            "reframe": "This time it wasn't my fault, but I will make sure to stock the shelves better to prevent this from happening again.",
        }
    ],
    "should statements": [
        {
            "situation": "The chef served me tomatoes on my pizza.",
            "thought": "The chef should know that I don't like them, and not put them on my pizza.",
            "reframe": "I don't like tomatoes so I have to make sure I tell the server next time not to put them on my pizza."
        },
        {
            "situation": "I am the youngest of 8 kids.",
            "thought": "I am the youngest of 8 kids and my older siblings should take care of me as the baby of the family.",
            "reframe": "I am the youngest of 8 kids. I always have someone to talk to.",
        },
        {
            "situation": "I'm single and 35.",
            "thought": "I'm still single at the age of 35, I should have been married and had a least one kid by now.",
            "reframe": "Though I'd like to be married, I have to remember that sooner or later I'll meet someone, I just have to wait for the right person.",
        }
    ]
}

"""
example usage: 

classifier_label = classifier.predict(user_input)              # e.g. "Fortune-telling"
exemplar_key = CLASSIFIER_LABEL_TO_EXEMPLAR_KEY[classifier_label]  # "fortune telling"
exemplars = [Example(**ex, category=exemplar_key) for ex in DEPLOYMENT_EXEMPLARS[exemplar_key]]
prompt = build_prompt("E4", thought=..., situation=..., category=exemplar_key, examples=exemplars)

"""