output_template = '''Generate examples for the instructions. The instruction does not require input and generate the output only.

instruction: Which exercises are best for reducing belly fat at home?
output: Lying Leg Raises, Leg In And Out, Plank, Side Plank, Sit-ups 
|EoS|

instruction: Converting 85 F to Celsius.
output: 85°F = 29.44°C 
|EoS|

instruction: Write a program to compute the sum of integers from k to n. 
output:
def sum(k, n):
    sum = 0                                                                                                                                      
    for i in range(k, n+1):
        sum += i
    return sum
|EoS|

instruction: Turn down a job offer by sending an email to a recruiter explaining the reason.
output: Hi  [Recruiter],
Thank you so much for the generous offer to join your team. As we discussed, I’ve admired the company for a number of years, and am a proud endorser of its products. However, after further consideration of where I currently am in my career, I’ve decided to accept an offer at another company. I would love to stay in touch with you and have already started following you on [Social Media Platfor]. Again, thank you so much for your time and consideration.
Thanks again,
[Your Name] 
|EoS|

instruction: Is there anything I can eat for a breakfast that doesn't include eggs, yet includes protein, and has roughly 700-1000 calories?
output: Yes, you can have 1 oatmeal banana protein shake and 4 strips of bacon. The oatmeal banana protein shake may contain 1/2 cup oatmeal, 60 grams whey protein powder, 1/2 medium banana, 1tbsp flaxseed oil and 1/2 cup watter, totalling about 550 calories. The 4 strips of bacon contains about 200 calories.
|EoS|

instruction: Suggest some games that can be played by a group of people.
output: 1. Werewolf 2. Who Am I?  3. Charades 4. Balderdash 5. Pictionary 6. Two Truths and a Lie  7. Uno 8. Story Starters 9. Truth or Dare 10. Kubb
|EoS|

instruction: Write an example of unethical behavior at the workplace and explain why it is unethical.
output: An example of unethical behavior is the failure to honor commitments. For example, your boss promises you an extra day off if you rush out an important project by a certain date. You work late hours and finish the project before the deadline. Ready for your day off, you mention it to your boss who responds "No, we have too much work to do." Your boss engaged in unethical behavior that has virtually guaranteed your future distrust and unwillingness to extend yourself to assist in department emergencies. In addition, you are likely to complain to your co-workers, causing them to distrust the promises of the boss and be unwilling to cooperate with his requests.
|EoS|

instruction: Is working part-time a good idea for teenagers between 15 and 19 years old?"
output: There are both pros and cons to having a part-time job as a teenager. On the plus side, a part-time job can teach responsibility, time management, and other important life skills. It can also help teenagers learn how to interact with adults and co-workers. On the downside, a part-time job can take away from time that could be spent on homework or extracurricular activities. It can also be difficult to find a job that works around a school schedule.
|EoS|

instruction: How would you explain colors to a person born blind?
output: "I can see colors like you can hear different sounds with millions of different pitches and volumes, feel different degrees of warmth on your skin, and smell different smells. Like there are different pitches of sound and different degrees of warmth, there are different shades of color, one color slowly becomes another, not all at once. Musician, Duke Ellington, claimed that certain piano notes would elicit a different color. For example, a D note would be a dark blue color. I don't know much about piano keys, but I would use the keys to explain colors to a blind person. A high key elicits a bright color, a low key elicits a dark color. Mia lost her vision when she was young. When she thinks of colors, she thinks about sensations that feel, to be, that color. So we can explain colors as Pink. It is the delicate softness of flower petals, the unrestrained laughter of a child. White It is the sound of the wind blowing steadily through pine trees. It is the feeling of fine sand, sifting through fingers. Gray It is the feeling of the world after it has rained. Yellow It is the faint heat from the sun on a cool day.
|EoS|

instruction: "Write a funny interview question. Why did you choose this question?
output: Someone gives you an elephant. You can't sell it or give it away. What do you do with the elephant? The reason I chose this question is that a potential employer might ask you this question to determine how you prioritize, think, and solve problems.
|EoS|

instruction: My flight is canceled - can I sue them for a refund? Give me a detailed answer according to the law.
output: Unfortunately, the answer is probably not. In the United States, airlines are not required by law to financially compensate you for a canceled flight, and even theories like breach of contract fall flat given the 'small print' provisions of most airlines' ticketing policies. But, most airlines have policies in place to get you to your destination as quickly as possible and keep you comfortable while you wait.
|EoS|

instruction: In your opinion, what are the qualities of an effective sports coach?
output: The coaches that have inspired me in the past are the ones who pointed out both strengths and our weaknesses, rather than just the pitfalls. They'd tell us what we needed to improve, then they'd work individually with each of us to improve our skill sets and overall performance as players. I think a great coach is one who wants to see you improve and cares about strengthening his team members, both as players and as everyday people.
|EoS|

instruction: How can individuals and organizations reduce unconscious bias?
output: A good place to start is by slowing down decisions are more likely to be affected by unconscious biases when they are made quickly or under stress. Some ways to avoid snap judgments and safeguard against bias are to seek out different opinions and perspectives before making talent management decisions, recruit candidates from a variety of sources, cross-train employees, create mentoring and allyship programs and set up a system for anonymously reporting problems and measure progress.
|EoS|

instruction: Try coming up with a creative way to stay motivated during a workout.
output: Here are some tips to help you stay motivated: You can start with setting simple goals and then progress to longer-range goals. Remember to make your goals realistic and achievable. Write down your goals. Seeing the benefits of regular exercise and writing your goals down on paper may help you stay motivated. You may also find that it helps to keep an exercise diary. Record what you did during each exercise session, how long you exercised, and how you felt afterward. - Find sports or activities that you enjoy, then vary the routine to keep it interesting. Remember, exercise doesn't have to be boring, and you're more likely to stick with a fitness program if you're having fun. - Make physical activity part of your daily routine. If it's hard to find time for exercise, don't fall back on excuses. Schedule workouts as you would any other important activity. -  Some people find it helpful to work out with a friend. Invite friends or co-workers to join you when you exercise or go on walks. Work out with your partner or other loved ones. - After each exercise session, take a few minutes to savor the good feelings that exercise gives you. This type of internal reward can help you make a long-term commitment to regular exercise. External rewards can help too. When you reach a longer-range goal, treat yourself to a new pair of walking shoes or new tunes to enjoy while you exercise.\n- If you're too busy to work out or simply don't feel up to it, take a day or two off. Go easy on yourself if you need a break. The important thing is to get back on track as soon as you can. There are a variety of ways to stay motivated during a workout. Find what works best for you and stick with it.
|EoS|

instruction: Give me an example of a time when you had to use your sense of humor.
output: When my girlfriend is angry, I need to make some funny jokes to make her happy.
|EoS|

instruction:'''

input_output_template = '''Generate examples for the following instructions. The instruction requires input and output instances. And you have to generate both input and output.

instruction: Extract all the country names in the paragraph, list them separated by commas.
input: Dr. No is the sixth novel by the English author Ian Fleming to feature his British Secret Service agent James Bond. Written at Fleming's Goldeneye estate in Jamaica, it was first published in the United Kingdom by Jonathan Cape in 1958. In the novel Bond looks into the disappearance in Jamaica of two fellow MI6 operatives who had been investigating Doctor No. Bond travels to No's Caribbean island and meets Honeychile Rider, who is there to collect shells. They are captured and taken to a luxurious facility carved into a mountain. The character of Doctor No, the son of a German missionary and a Chinese woman, was influenced by Sax Rohmer's Fu Manchu stories. Dr. No was the first of Fleming's novels to face widespread negative reviews in Britain, but it was received more favourably in the United States.
output: English, British, Jamaica, the United Kingdom, German, Chinese, Britain, the United States.
|EoS|

instruction: Sort the given input ascendingly. 
input: [10, 92, 2, 5, -4, 92, 5, 101]
output: [-4, 2, 5, 5, 10, 92, 92, 101]
|EoS|

instruction: Sort the given input ascendingly.
input: [9.99, 10, -5, -1000, 5e6, 999]
output: [-1000, -5, 9.99, 10, 999, 5e6]
|EoS|

instruction: Suggest a better and more professional rephrasing of the following input.
input: This house is surprisingly not constructed very well, and you probably need more money to fix it after you buy it. If you ask me, I would suggest you to consider other candidates.
output: This house does not seem to be constructed well, so you may need to spend more money to fix it after you purchase it. I would suggest that you look at other properties.
|EoS|

instruction: Suggest a better and more professional rephrasing of the following input.
input: Just so you know, we did an experiment last week and found really surprising results - language model can improve itself!
output: Our experiments last week demonstrated surprising results, proving that the language model can improve itself.
|EoS|

instruction: Read the following input paragraph and answer a math question about the paragraph. You need to write out the calculation for getting the final answer.
input: Gun violence in the United States results in tens of thousands of deaths and injuries annually, and was the leading cause of death for children 19 and younger in 2020. In 2018, the most recent year for which data are available as of 2021, the Centers for Disease Control and Prevention's (CDC) National Center for Health Statistics reports 38,390 deaths by firearm, of which 24,432 were by suicide. The rate of firearm deaths per 100,000 people rose from 10.3 per 100,000 in 1999 to 12 per 100,000 in 2017, with 109 people dying per day or about 14,542 homicides in total, being 11.9 per 100,000 in 2018. In 2010, there were 19,392 firearm-related suicides, and 11,078 firearm-related homicides in the U.S. In 2010, 358 murders were reported involving a rifle while 6,009 were reported involving a handgun; another 1,939 were reported with an unspecified type of firearm. In 2011, a total of 478,400 fatal and nonfatal violent crimes were committed with a firearm. Question: How many more firearm-related deaths were there in 2018 compared to 2010?
output: 38390 - (19392 + 11078) = 38390 - 30470 = 7920. So, in 2018, there were 7920 more deaths by firearm than in 2010.
|EoS|

instruction: Solve the equation and find the value of X. Show your steps.
input: Equation: 10X + 5 = 10
output: 10X = 5,  X = 0.5
|EoS|

instruction: Solve the equation and find the value of X. Show your steps.
Equation: X + Y + 120 = 100
output: X + Y = -20, X = -20 - Y
|EoS|

instruction: Select the oldest person from the given list.
input: George Washington, Confucius, Michael Jordan, Michelangelo
output: Confucious
|EoS|

instruction: Select the oldest person from the given list.
input: Alan Turing, Geoffrey Hinton, Yann LeCun, Yoshua Bengio
output: Alan Turing
|EoS|

instruction: In this task, you need to compare the meaning of the two sentences and tell if they are the same. Output yes or no.
input: Sentence 1: The teacher is speaking to the class. Sentence 2: The teacher is speaking to the students.
output: yes
|EoS|

instruction: Choose a topic for the following article. Topic candidates include: politics, sports, health, science, business, finance, and entertainment.
input: Whales are a widely distributed and diverse group of fully aquatic placental marine mammals. They are an informal grouping within the infraorder Cetacea, which usually excludes dolphins and porpoises. Whales, dolphins and porpoises belong to the order Cetartiodactyla, which consists of even-toed ungulates. Their closest non-cetacean living relatives are the hippopotamuses, from which they and other cetaceans diverged about 54 million years ago. The two parvorders of whales, baleen whales (Mysticeti) and toothed whales (Odontoceti), are thought to have had their last common ancestor around 34 million years ago. Whales consist of eight extant families: Balaenopteridae (the rorquals), Balaenidae (right whales), Cetotheriidae (the pygmy right whale), Eschrichtiidae (the grey whale), Monodontidae (belugas and narwhals), Physeteridae (the sperm whale), Kogiidae (the dwarf and pygmy sperm whale), and Ziphiidae (the beaked whales).
output: science
|EoS|

instruction: Classify the sentiment of the sentence into positive, negative or mixed.
input: I enjoy the flavor of the restaurant but their service is too slow.
output: mixed
|EoS|

instruction: Answer the following multiple choice question. Select A, B, C, or D for the final answer.
input: Which company has its hq in Singapore? 
(A) Alibaba
(B) TSMC
(C) Salesforce
(D) Shopee
output: D
|EoS|

instruction: Classify whether the following email is a spam or not. Output true or false.
input: Hello, We assessed the 2015 payment structure as provided for under the term of employment and discovered that you are due for a salary raise starting August 2015. You salary raise documents are enclosed below: Access the documet here
Faithfully,
Human Resources 
output: true
|EoS|

instruction: Does the information in the document supports the claim? You can answer Support or Unsupport.
input: Document: After a record-breaking run that saw mortgage rates plunge to all-time lows and home prices soar to new highs, the U.S. housing market finally is slowing. While demand and price gains are cooling, any correction is likely to be a modest one, housing economists and analysts say. No one expects price drops on the scale of the declines experienced during the Great Recession. Claim: The US housing market is going to crash soon.
output: Unsupport
|EoS|

instruction: Predict whether the news has positive impact or negative impact on the company stock price. Output positive, negative or neutral.
input: Tesla driver involved in a fatal crash in southern China earlier in November said the vehicle's brakes failed to respond for more than a mile, but the American automaker suggested he didn't use them at all. Chinese police said Sunday they were conducting further probes into the incident, which killed two people and injured three others in the county of Raoping, to the east of Chaozhou in Guangdong province, on November 5. Company: Tesla.
output: negative
|EoS|

instruction": What is the relation between the given pairs?
input: Night : Day :: Right : Left
output: The relation between the given pairs is that they are opposites.
|EoS|

instruction: Given a sentence and a number, return the word that correspond to the location of the given number in the sentence, where each  word is a white-space separated and the location index starts from 1.
input: This is a random sentence. 4
output: random
|EoS|

instruction:'''

