FROM python:3.8
ENV JAVA_HOME /usr/lib/jvm/java-1.7-openjdk/jre
RUN apt-get update && apt-get install -y g++ default-jdk
COPY requirements.txt /root 
RUN pip install -r /root/requirements.txt

# Install packages for building ruby
RUN apt-get update
RUN apt-get install -y --force-yes build-essential curl git
RUN apt-get install -y --force-yes zlib1g-dev libssl-dev libreadline-dev libyaml-dev libxml2-dev libxslt-dev
RUN apt-get clean

# Install rbenv and ruby-build
RUN git clone https://github.com/sstephenson/rbenv.git /root/.rbenv
RUN git clone https://github.com/sstephenson/ruby-build.git /root/.rbenv/plugins/ruby-build
RUN /root/.rbenv/plugins/ruby-build/install.sh
ENV PATH /root/.rbenv/bin:$PATH
RUN echo 'eval "$(rbenv init -)"' >> /etc/profile.d/rbenv.sh # or /etc/profile
RUN echo 'eval "$(rbenv init -)"' >> .bashrc

CMD source ~/.bashrc
RUN rbenv install 2.7.6 
RUN rbenv global 2.7.6
CMD gem install wp2txt
