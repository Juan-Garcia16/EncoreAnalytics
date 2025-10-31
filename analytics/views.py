from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, Sum, Value, DecimalField
from django.db.models.functions import Coalesce
from django.shortcuts import render
import json

from conciertos.models import Concert, SetlistEntry
from fans.models import Interest, Attendance



class AnalyticsDashboardView(TemplateView):
	template_name = 'analytics/dashboard.html'

	def get(self, request, *args, **kwargs):
		# 1) Canciones más interpretadas (Setlist frequency)
		songs_qs = (
			SetlistEntry.objects.values('song__id', 'song__title')
			.annotate(count=Count('pk'))
			.order_by('-count')[:10]
		)
		songs_labels = [row['song__title'] for row in songs_qs]
		songs_data = [row['count'] for row in songs_qs]

		# 2) Conciertos por ciudad
		concerts_by_city = (
			Concert.objects.filter(venue__city__name__isnull=False)
			.values('venue__city__name', 'venue__city__country')
			.annotate(count=Count('pk'))
			.order_by('-count')[:10]
		)
		city_labels = [f"{r['venue__city__name']}, {r['venue__city__country']}" for r in concerts_by_city]
		city_data = [r['count'] for r in concerts_by_city]

		# 3) Artistas con más conciertos
		artists_qs = (
			Concert.objects.values('artist__id', 'artist__name')
			.annotate(count=Count('pk'))
			.order_by('-count')[:10]
		)
		artist_labels = [r['artist__name'] for r in artists_qs]
		artist_data = [r['count'] for r in artists_qs]

		# 4) Conciertos más esperados (por número de interest)
		expected_qs = (
			Interest.objects.values('concert__id', 'concert__artist__name', 'concert__venue__city__name', 'concert__start_datetime')
			.annotate(count=Count('pk'))
			.order_by('-count')[:10]
		)
		expected_labels = [f"{r['concert__artist__name']} — {r['concert__venue__city__name']}" for r in expected_qs]
		expected_data = [r['count'] for r in expected_qs]

		# 5) Promedio de calificaciones por artista
		ratings_qs = (
			Attendance.objects.filter(rating__isnull=False)
			.values('concert__artist__id', 'concert__artist__name')
			.annotate(avg_rating=Avg('rating'), count=Count('pk'))
			.order_by('-avg_rating')[:10]
		)
		ratings_labels = [r['concert__artist__name'] for r in ratings_qs]
		ratings_data = [round(float(r['avg_rating'] or 0), 2) for r in ratings_qs]

		# 6) Ingresos totales por artista
		income_qs = (
			Concert.objects.values('artist__id', 'artist__name')
			# ensure Coalesce returns a Decimal-compatible type by giving Value a DecimalField output
			.annotate(total_income=Coalesce(Sum('total_income'), Value(0, output_field=DecimalField())))
			.order_by('-total_income')[:10]
		)
		income_labels = [r['artist__name'] for r in income_qs]
		# ensure numeric floats and sort descending by total_income
		income_list = [(r['artist__name'], float(r['total_income'] or 0)) for r in income_qs]
		# already ordered by -total_income, but be safe
		income_list.sort(key=lambda x: x[1], reverse=True)
		income_labels = [x[0] for x in income_list]
		income_data = [x[1] for x in income_list]

		context = {
			'songs_labels': json.dumps(songs_labels, ensure_ascii=False),
			'songs_data': json.dumps(songs_data),
			'songs_count': len(songs_data),
			'city_labels': json.dumps(city_labels, ensure_ascii=False),
			'city_data': json.dumps(city_data),
			'city_count': len(city_data),
			'artist_labels': json.dumps(artist_labels, ensure_ascii=False),
			'artist_data': json.dumps(artist_data),
			'artist_count': len(artist_data),
			'expected_labels': json.dumps(expected_labels, ensure_ascii=False),
			'expected_data': json.dumps(expected_data),
			'expected_count': len(expected_data),
			'ratings_labels': json.dumps(ratings_labels, ensure_ascii=False),
			'ratings_data': json.dumps(ratings_data),
			'ratings_count': len(ratings_data),
			'income_labels': json.dumps(income_labels, ensure_ascii=False),
			'income_data': json.dumps(income_data),
			'income_count': len(income_data),
		}
		return render(request, self.template_name, context)
