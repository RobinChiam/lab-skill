# Introducing the `/lab` skill

This skill is designed to run alongside Matt Pocock's [`/teach`](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md) skill.

## What does `/teach` do?

The `/teach` skill uses HTML lessons and interactive exercises, such as quizzes with immediate feedback, to help you learn and assess your understanding of a topic.

## What does `/lab` do?

The `/lab` skill extends `/teach` by creating a lab environment in its own directory and presenting the learner with a scenario that requires them to apply what they have learned. It includes a worked example based on a similar scenario that requires the same skills.

The learner can refer to the worked example if they get stuck while attempting the lab scenario.

The `/lab` skill also instructs the AI agent running the `/teach` session to use the learner's lab progress and results to inform its assessment of their understanding and create the corresponding learning record.

## What frameworks were considered?

Matt Pocock's `/teach` skill uses the Zone of Proximal Development to guide teaching based on what a learner can do independently, what they can do with guidance, and what they cannot yet do. This helps the agent select suitable tasks and support for the learner.

## Bloom's Revised Taxonomy 2001
> In 1956, original version of the taxonomy was 6 levels of objectives;
>
> Knowledge -> Comprehension -> Application -> Analysis -> Synthesis -> Evaluation
>
> In 2001, it was revised with some adjustments and each level was renamed;
>
> Remember -> Understand -> Apply -> Analyze -> Evaluate -> Create

<img src="https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6a/Bloom%27s_revised_taxonomy.svg/960px-Bloom%27s_revised_taxonomy.svg.png?utm_source=en.wikipedia.org&utm_campaign=imageinfo&utm_content=thumbnail" alt="bloom-revised-taxonomy-2001-version.png" width="500">

#### Breakdown of each level 
1. Knowledge / Remember: 
	Recognizing or recalling facts, terms, basic concepts or answers without necessarily understanding their meaning.
2. Comprehension / Understand: 
	Demonstrating an understanding of facts and ideas by organizing and summarizing information.
3. Application / Apply: 
	Using acquired knowledge to solve problems in new or unfamiliar situations.
4. Analysis / Analyze: 
	Breaking down information into parts to understand relationships, motives or causes.
5. Synthesis / Create: 
	Building a new whole by combining elements or creating new meaning.
6. Evaluation / Evaluate: 
	Making judgements about information, based on set criteria or standards.


## What is the expected outcome?

The goal is to help learners strengthen their theoretical and practical understanding of a topic or skill and apply what they learn independently.
