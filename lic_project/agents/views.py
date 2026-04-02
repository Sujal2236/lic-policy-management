from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Agent, PolicyHolder
from django.db.models import Sum

def index(request):
    query = request.GET.get('q')

    if query:
        agents = Agent.objects.filter(
            Q(name__icontains=query) | Q(phone__icontains=query)
        )
    else:
        agents = Agent.objects.all()

    return render(request, 'index.html', {'agents': agents})


def add_agent(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        policy_number = request.POST.get('policy_number')
        total_amount = request.POST.get('total_amount')
        policy_years = int(request.POST.get('policy_years'))
        payment_interval = int(request.POST.get('plan_duration'))
        start_date = date.fromisoformat(request.POST.get('start_date'))

        # Calculate dates
        next_due_date = calculate_next_due(start_date, payment_interval)
        maturity_date = start_date + relativedelta(years=policy_years)

        # Create Agent
        agent = Agent.objects.create(
            name=name,
            phone=phone
        )

        # Create Policy
        PolicyHolder.objects.create(
            agent=agent,
            policy_number=policy_number,
            holder_name=name,
            phone=phone,
            email=email,
            total_amount=total_amount,
            policy_years=policy_years,
            start_date=start_date,
            payment_interval=payment_interval,
            next_due_date=next_due_date,
            maturity_date=maturity_date
        )

        return redirect('/')

    return render(request, "add.html")


def update_agent(request, id):
    agent = get_object_or_404(Agent, id=id)
    policy = PolicyHolder.objects.filter(agent=agent).first()

    if request.method == "POST":
        agent.name = request.POST.get("name")
        agent.phone = request.POST.get("phone")
        agent.save()

        if policy:
            policy.policy_number = request.POST.get("policy_number")
            policy.total_amount = request.POST.get("total_amount")
            policy.email = request.POST.get("email")

            start_date = date.fromisoformat(request.POST.get("start_date"))
            payment_interval = int(request.POST.get("plan_duration"))
            policy_years = int(request.POST.get("policy_years"))

            policy.start_date = start_date
            policy.payment_interval = payment_interval
            policy.policy_years = policy_years

            # Recalculate dates
            policy.next_due_date = calculate_next_due(start_date, payment_interval)
            policy.maturity_date = start_date + relativedelta(years=policy_years)

            policy.save()

        return redirect("/")

    return render(request, "update.html", {"agent": agent, "policy": policy})


def delete_agent(request, id):
    agent = get_object_or_404(Agent, id=id)
    agent.delete()
    return redirect('/')


def calculate_next_due(start_date, payment_interval):
    today = date.today()
    next_due = start_date

    while next_due <= today:
        next_due += relativedelta(months=payment_interval)

    return next_due

def dashboard(request):
    today = date.today()
    six_months_later = today + relativedelta(months=6)

    # Stat 1: total policies
    total_policies = PolicyHolder.objects.count()

    # Stat 2: total amount
    total_amount = PolicyHolder.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Stat 3: policies added this month
    this_month_policies = PolicyHolder.objects.filter(
        start_date__year=today.year,
        start_date__month=today.month
    )

    # Stat 4: upcoming maturities in next 6 months
    upcoming_maturities = PolicyHolder.objects.filter(
        maturity_date__gte=today,
        maturity_date__lte=six_months_later
    ).order_by('maturity_date')

    return render(request, 'dashboard.html', {
        'total_policies': total_policies,
        'total_amount': total_amount,
        'this_month_policies': this_month_policies,
        'upcoming_maturities': upcoming_maturities,
        'today': today,
    })