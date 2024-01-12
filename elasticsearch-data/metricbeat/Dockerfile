FROM ubuntu:latest

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-7.5.0-amd64.deb \
    && dpkg -i metricbeat-7.5.0-amd64.deb \
    && rm metricbeat-7.5.0-amd64.deb

COPY metricbeat.yml /usr/share/metricbeat/metricbeat.yml

RUN chmod 644 /usr/share/metricbeat/metricbeat.yml

CMD ["metricbeat", "-e"]
