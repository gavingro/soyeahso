from typing import Optional, List
import random

import ell


def get_quality_icebreaker_questions(
    n_seeded_questions: int = 5,
    previously_asked_questions: Optional[List[str]] = None,
    **kwargs,
) -> List[str]:
    """
    Generate 3 quality icebreaker questions.

    Parameters
    ----------
    n_seeded_questions : int, optional
        Number of questions to initially prune down from, by default 5
    previously_asked_questions : Optional[List[str]], optional
        Text of previously genearated questions to avoid, by default None

    Returns
    -------
    str
        Question Text, generated.
    """

    initial_questions = brainstorm_icebreaker_questions(
        n_questions=n_seeded_questions,
        previous_questions_text=(
            "[" "]\n[".join(previously_asked_questions) + "]"
            if previously_asked_questions
            else None
        ),
        **kwargs,
    )
    question_list = extract_questions(initial_questions)
    n_questions_to_shave = len(question_list) // 5
    # Get rid of gnarly personal questions lol.
    for _ in range(n_questions_to_shave):
        question_list.pop(-1)
    selected_questions = random.sample(
        population=extract_questions(initial_questions), k=3
    )
    plain_questions = plainify_questions("\n".join(selected_questions), **kwargs)
    return extract_questions(plain_questions)


@ell.simple(model="gpt-4o-mini", temperature=1.2, top_p=0.9)
def brainstorm_icebreaker_questions(
    n_questions: int, previous_questions_text: Optional[str] = None
):
    """
    You are a researcher helping design questions to create relationships
    between new friends.
    Your subjects are two classmates that sit next to each other and spend lots
    of time together, but are NOT close to each other emotionally.
    There is an awkward silence between them,
    but they both want to get to know each other.

    You should NOT speak like "chatgpt",
    but instead you should sound like a casual professor teaching a course
    to put your test subjects at ease.
    """
    initial_prompt = (
        f"Can you ask {n_questions} 'icebreaker' questions, "
        "each designed to spark a conversation "
        "to fill the downtime before the next class begins for the two classmates? "
        "Be careful to ensure that the questions don't take too much effort and brainpower "
        "to answer -- after all, we're just chatting, not coming up with essay prompts or therapy questions. "
        "Multiple choice questions with two answers that reveal emotional preferences are great, but "
        "try to make it seem like they are open ended questions. "
        "You can ask proper open ended questions instead of multiple choice questions if you want, but make sure they are easy to answer, like "
        "around peoples favourite or least favourite things. This shouldn't feel like an interview. "
        "Some fun open questions might start with 'Why do you think that' in order to illicit peoples preferences. "
        f"Each of the {n_questions} questions should be more intimate "
        "and personal than the last question, "
        "with question number 1 being a fairly comfortable question "
        f"and question number {n_questions} being fairly prying. "
        "Try to be creative with your questions, don't just ask the same ones another researcher would ask. "
        "Be sure to separate each question with square brackets, like the following: "
        "[Question 1?]\n [Question 2?] \n\n"
        "Do not include anything other than the questions in the square brackets."
    )
    if not previous_questions_text:
        return initial_prompt

    follow_up_prompt = (
        f"That's a great start! Please ask {n_questions} more 'icebreaker' questions in the same way, "
        "each different from the previously asked questions. "
        "Be sure to separate each question with square brackets, like the following: "
        "[Question 1?]\n [Question 2?] \n\n"
        "Do not include anything other than the questions in the square brackets."
    )
    return [
        ell.user(initial_prompt),
        ell.assistant(previous_questions_text),
        ell.user(follow_up_prompt),
    ]


@ell.simple(model="gpt-4o-mini", temperature=1.0, top_p=0.6)
def plainify_questions(
    questions_text: str,
) -> str:
    """
    You and I are classmates with 5 minutes of down time before our
    next class.
    You should NOT speak like "chatgpt",
    but instead you should sound like a normal girl
    taking a post-secondary university course with me.
    """
    return (
        "Here are a few icebreaker questions I heard from a friend. "
        "Each of them is a question enclosed in square brackets, like this: "
        "[Question 1?]\n [Question 2?] \n\n"
        "But like, they are pretty formal, and I think a chatbot came up with them. "
        "Can you help me out and ask them to me in plain language like we'd normally use in class? "
        "I'd love for you to add your own style and put your own spin on them as well! "
        "It'd still be super helpful if you could put the questions in square brackets like they came in, "
        " and not say anything else other than the questions. "
        f"Here are the questions: \n {questions_text}"
    )


@ell.simple(model="gpt-4o-mini", temperature=0.5, top_p=0.3)
def select_3_best_questions(
    questions_text: str,
) -> str:
    """
    You are the teenage chaparone for your two best friends on a date.
    Your two best friends don't know each other very well, but they want to get to know each other.
    There is an awkward silence between them, and they need you to ask them a question.
    You want to help them show vulnarability to each other, but not too much vulnarability
    that they will be uncomfortable and afraid of being judged.
    """
    return (
        "Here are a few icebreaker questions I heard from a friend. "
        "Each of them is a question enclosed in square brackets, like [Question?]. "
        "But like, some of them might be too boring, and some of them might be too scary for these two strangers on a date. "
        "Could you help select the 3 most interesting questions that would be ideal for breaking the tension on the date? "
        "I'd love for you to add your own style and put your own spin on them as well! "
        "Try to pick creative questions that sound novel, but also easy to answer. "
        "It'd still be super helpful if you could put the questions in square brackets like they came in, "
        " and not say anything else other than the questions. "
        f"Here are the questions: \n {questions_text}"
    )


def extract_questions(question_text) -> list:
    """Extract [square enclosed] questions from text_string"""
    question_strings = question_text.split("[")
    questions = [q.strip().strip("]") for q in question_strings[1:]]
    return questions
