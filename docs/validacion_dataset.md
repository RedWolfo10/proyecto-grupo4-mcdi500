# Validación del dataset — MCDI500

**Archivo:** `listings.csv` · 5106 filas × 90 columnas

## Perfil de variables

| variable | dtype | rol | unicos | pct_nulos |
| --- | --- | --- | --- | --- |
| id | int64 | identificador | 5106 | 0.0 |
| listing_url | str | identificador | 5106 | 0.0 |
| scrape_id | int64 | discreta | 1 | 0.0 |
| last_scraped | str | binaria | 2 | 0.0 |
| source | str | nominal | 1 | 95.3 |
| name | str | identificador | 4990 | 0.0 |
| description | str | texto libre | 4720 | 0.6 |
| neighborhood_overview | float64 | vacía | 0 | 100.0 |
| picture_url | str | texto libre | 5077 | 0.0 |
| host_id | int64 | continua | 3609 | 0.0 |
| host_url | str | alta cardinalidad | 3609 | 0.0 |
| host_profile_id | int64 | continua | 3609 | 0.0 |
| host_profile_url | str | alta cardinalidad | 3609 | 0.0 |
| host_name | str | alta cardinalidad | 1617 | 0.0 |
| host_since | float64 | vacía | 0 | 100.0 |
| hosts_time_as_user_years | int64 | discreta | 18 | 0.0 |
| hosts_time_as_user_months | int64 | discreta | 12 | 0.0 |
| hosts_time_as_host_years | int64 | discreta | 16 | 0.0 |
| hosts_time_as_host_months | int64 | discreta | 12 | 0.0 |
| host_location | str | alta cardinalidad | 189 | 32.0 |
| host_about | str | texto libre | 1559 | 50.6 |
| host_response_time | float64 | vacía | 0 | 100.0 |
| host_response_rate | float64 | vacía | 0 | 100.0 |
| host_acceptance_rate | float64 | vacía | 0 | 100.0 |
| host_is_superhost | str | binaria | 2 | 0.0 |
| host_thumbnail_url | float64 | vacía | 0 | 100.0 |
| host_picture_url | str | texto libre | 3440 | 0.0 |
| host_neighbourhood | float64 | vacía | 0 | 100.0 |
| host_listings_count | int64 | discreta | 72 | 0.0 |
| host_total_listings_count | float64 | vacía | 0 | 100.0 |
| host_verifications | float64 | vacía | 0 | 100.0 |
| host_has_profile_pic | str | binaria | 2 | 0.0 |
| host_identity_verified | str | binaria | 2 | 0.0 |
| neighbourhood | float64 | vacía | 0 | 100.0 |
| neighbourhood_cleansed | str | alta cardinalidad | 32 | 0.0 |
| neighbourhood_group_cleansed | float64 | vacía | 0 | 100.0 |
| latitude | float64 | continua | 4200 | 0.0 |
| longitude | float64 | continua | 4264 | 0.0 |
| property_type | str | alta cardinalidad | 53 | 0.0 |
| room_type | str | nominal | 4 | 0.0 |
| accommodates | int64 | discreta | 16 | 0.0 |
| bathrooms | float64 | vacía | 0 | 100.0 |
| bathrooms_text | str | alta cardinalidad | 28 | 0.1 |
| bedrooms | float64 | discreta | 12 | 0.0 |
| beds | float64 | discreta | 17 | 1.1 |
| amenities | str | texto libre | 4968 | 0.0 |
| price | str | alta cardinalidad | 3297 | 4.7 |
| price_quote_checkin_date | str | fecha | 170 | 3.2 |
| price_quote_checkout_date | str | fecha | 207 | 3.2 |
| price_quote_total_price | float64 | continua | 3347 | 4.7 |
| price_quote_price_per_night | float64 | continua | 3297 | 4.7 |
| price_quote_raw | str | texto libre | 4545 | 3.2 |
| minimum_nights | float64 | discreta | 38 | 0.0 |
| maximum_nights | float64 | discreta | 82 | 0.0 |
| minimum_minimum_nights | float64 | discreta | 38 | 0.0 |
| maximum_minimum_nights | float64 | discreta | 42 | 0.0 |
| minimum_maximum_nights | float64 | discreta | 82 | 0.0 |
| maximum_maximum_nights | float64 | discreta | 82 | 0.0 |
| minimum_nights_avg_ntm | float64 | continua | 109 | 0.0 |
| maximum_nights_avg_ntm | float64 | continua | 136 | 0.0 |
| calendar_updated | float64 | vacía | 0 | 100.0 |
| has_availability | str | nominal | 1 | 0.9 |
| availability_30 | int64 | discreta | 31 | 0.0 |
| availability_60 | int64 | discreta | 61 | 0.0 |
| availability_90 | int64 | discreta | 91 | 0.0 |
| availability_365 | int64 | continua | 350 | 0.0 |
| calendar_last_scraped | str | binaria | 2 | 0.0 |
| number_of_reviews | int64 | continua | 332 | 0.0 |
| number_of_reviews_ltm | int64 | discreta | 127 | 0.0 |
| number_of_reviews_l30d | int64 | discreta | 17 | 0.0 |
| availability_eoy | int64 | discreta | 99 | 0.0 |
| number_of_reviews_ly | int64 | discreta | 115 | 0.0 |
| estimated_occupancy_l365d | int64 | discreta | 73 | 0.0 |
| estimated_revenue_l365d | float64 | continua | 3306 | 4.7 |
| first_review | str | fecha | 1880 | 14.7 |
| last_review | str | fecha | 699 | 14.7 |
| review_scores_rating | float64 | continua | 110 | 14.7 |
| review_scores_accuracy | float64 | continua | 103 | 14.7 |
| review_scores_cleanliness | float64 | continua | 123 | 14.7 |
| review_scores_checkin | float64 | continua | 88 | 14.7 |
| review_scores_communication | float64 | continua | 100 | 14.7 |
| review_scores_location | float64 | continua | 109 | 14.7 |
| review_scores_value | float64 | continua | 111 | 14.7 |
| license | str | alta cardinalidad | 44 | 99.0 |
| instant_bookable | float64 | vacía | 0 | 100.0 |
| calculated_host_listings_count | int64 | discreta | 54 | 0.0 |
| calculated_host_listings_count_entire_homes | int64 | discreta | 54 | 0.0 |
| calculated_host_listings_count_private_rooms | int64 | discreta | 19 | 0.0 |
| calculated_host_listings_count_shared_rooms | int64 | discreta | 4 | 0.0 |
| reviews_per_month | float64 | continua | 751 | 14.7 |

## Requisitos del curso

| estado | requisito | detalle |
| --- | --- | --- |
| OK | Al menos 2000 filas | 5106 filas |
| OK | Al menos 12 columnas | 90 columnas |
| OK | Combina al menos 3 roles analíticos | discreta, continua, alta cardinalidad, texto libre, binaria, fecha, nominal |
| OK | Al menos una variable numérica | 46 numéricas (continuas o discretas) |
| OK | Al menos una variable categórica | 8 categóricas (nominales, binarias u ordinales) |
| OK | Presencia de valores faltantes | máximo 100.0% en una variable |
| AVISO | Ninguna variable sobre 60% de faltantes | máximo 100.0% |
| OK | Incluye alguna variable de fecha | 4 detectadas |
| OK | Incluye texto o categórica de alta cardinalidad | 15 detectadas |
| OK | Archivo bajo 100 MB | 13.6 MB |
| OK | Sin filas duplicadas exactas | ninguna |

## Resultado

El conjunto **cumple** los requisitos mínimos.