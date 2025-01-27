from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from taxi.models import Car, Driver, Manufacturer


def index(request: HttpRequest) -> HttpResponse:
    num_drivers = Driver.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_cars = Car.objects.count()
    num_visits = request.session.get("num_visits", 0)
    num_visits += 1
    request.session["num_visits"] = num_visits
    context = {
        "num_drivers": num_drivers,
        "num_manufacturers": num_manufacturers,
        "num_cars": num_cars,
        "num_visits": num_visits,
    }
    return render(
        request,
        "taxi/index.html",
        context=context
    )


class ManufacturerListView(ListView):
    model = Manufacturer
    queryset = Manufacturer.objects.all().order_by("name")
    paginate_by = 5


class ManufacturerCreateView(LoginRequiredMixin, CreateView):
    model = Manufacturer
    fields = "__all__"
    template_name = "taxi/manufacturer_form.html"

    def get_success_url(self):
        return reverse("taxi:manufacturer-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referer_url = self.request.META.get("HTTP_REFERER", "/")
        context["previous"] = referer_url
        return context


class ManufacturerUpdateView(LoginRequiredMixin, UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/manufacturer_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referer_url = self.request.META.get("HTTP_REFERER", "/")
        context["previous"] = referer_url
        return context


class ManufacturerDeleteView(LoginRequiredMixin, DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/manufacturer_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referer_url = self.request.META.get("HTTP_REFERER", "/")
        context["previous"] = referer_url
        return context


class CarListView(ListView):
    model = Car
    queryset = Car.objects.select_related("manufacturer")
    paginate_by = 5


class CarDetailView(LoginRequiredMixin, DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/car_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referer_url = self.request.META.get("HTTP_REFERER", "/")
        context["previous"] = referer_url
        return context


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    fields = "__all__"
    template_name = "taxi/car_form.html"

    def get_success_url(self):
        return reverse("taxi:car-detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referer_url = self.request.META.get("HTTP_REFERER", "/")
        context["previous"] = referer_url
        return context


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/car_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referer_url = self.request.META.get("HTTP_REFERER", "/")
        context["previous"] = referer_url
        return context


class DriverListView(ListView):
    model = Driver
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = self.request.user
        return context


class DriverDetailView(LoginRequiredMixin, DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars")