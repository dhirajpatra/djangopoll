import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice, User


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_fail_to_create_question_without_any_choice_text(self):
        """
        try to create question witout any Choice
        """
        response = create_question([], question_text="Current question.", days=1)
        self.assertEqual(response, "At least one choice_text required.")

    def test_fail_to_create_question_with_more_than_ten_choice_text(self):
        """
        try to create question witout any Choice
        """
        choice_text = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
        response = create_question(choice_text, question_text="Current question.", days=1)
        self.assertEqual(response, "Max ten choice_text can be added.")


def create_question(choice_text, question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    if not choice_text:
        return "At least one choice_text required."
    elif len(choice_text) > 10:
        return "Max ten choice_text can be added."
    time = timezone.now() + datetime.timedelta(days=days)
    q = Question.objects.create(question_text=question_text, pub_date=time, ip_address="127.0.0.1")
    Choice.objects.create(question_id=q.id, choice_text=choice_text)
    return q


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available for you.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page. Taking local IP default.
        """
        create_question(["good choice"], question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page. Taking local IP default.
        """
        create_question(["good choice"], question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available for you.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed. Taking local IP default.
        """
        create_question(["good choice"], question_text="Past question.", days=-30)
        create_question(["good choice"], question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions. Taking local IP default.
        """
        create_question(["good choice"], question_text="Past question 1.", days=-30)
        create_question(["good choice"], question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(["good choice"], question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_question_already_display_for_ip(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(["good choice"], question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text. Taking local IP default.
        """
        past_question = create_question(["good choice"], question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class VoteTest(TestCase):

    def test_success_vote(self):
        """
        Test a successful vote on a question with IP
        """
        question = create_question(["good choice"], question_text='Current Question.', days=-1)
        response = vote("127.0.0.1", question)
        self.assertEqual(response, True)

    def test_vote_question_user_already_voted(self):
        """
        The question will not be voted for to the same IP/user
        if IP/user already voted for the same question.
        """
        ip = "127.0.0.1"
        question = create_question(["good choice"], question_text='Current Question.', days=-1)
        response = vote(ip, question)
        # again trying to vote
        response = vote(ip, question)
        self.assertEqual(response, False)


def vote(ip, question):
    """vote on question and udpate the IP address for that user voted"""
    already_voted = User.objects.filter(question_id=question.id)
    if not already_voted:
        selected_choice = question.choice_set.get(pk=question.id)
        selected_choice.votes += 1
        selected_choice.save()
        User.objects.create(question=question, ip_address=ip)
        return True
    return False
