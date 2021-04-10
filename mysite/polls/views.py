from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from ipware import get_client_ip

from .models import Choice, Question, User
from .forms import QuestionForm, ChoiceFormSet


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future). Already shown to this user questions not included.
        """
        ip, is_routable = get_client_ip(self.request)
        if ip is not None:
            questions = Question.objects.exclude(user__ip_address=ip).filter(
                    pub_date__lte=timezone.now()
                ).order_by('-pub_date')[:5]
        return questions


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def poll_new(request):
    """create new poll question"""
    msg = ''
    if request.method == "POST":
        question_form = QuestionForm(request.POST or None)
        formset = ChoiceFormSet(request.POST or None)
        if question_form.is_valid() and formset.is_valid:
            ip, is_routable = get_client_ip(request)
            try:
                if ip is not None:
                    print(f"***User with IP {ip} creating a new question: {request.POST['question_text']}***")
                    question = question_form.save(commit=False)
                    question.ip_address = ip
                    question.pub_date = timezone.now()
                    question.save()
                    i = 0
                    flag = 0
                    for form in formset:
                        if form.is_valid() and form.data['form-' + str(i) + '-choice_text'] != '':
                            choice = form.save(commit=False)
                            choice.question_id = question.id
                            choice.save()
                            flag = 1
                        i += 1
                    if flag == 0:
                        Question.objects.get(pk=question.id).delete()
                    msg = 'Question successfully saved'
                else:
                    msg = "IP is not tracked"
            except (KeyError, (Question.DoesNotExist or Choice.ViewDoesNotExist)):
                return render(request, 'polls/new.html', {'question_form': question_form, 'formset': formset, 'msg': 'Question not saved'})
    question_form = QuestionForm()
    formset = ChoiceFormSet()
    return render(request, 'polls/new.html', {'question_form': question_form, 'formset': formset, 'msg': msg})


def vote(request, question_id):
    """vote on question and udpate the IP address for that user voted"""
    ip, is_routable = get_client_ip(request)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print(f"***User with IP {ip} voted to question: {question}***")
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        ip, is_routable = get_client_ip(request)
        if ip is not None:
            User.objects.create(question=question, ip_address=ip)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
