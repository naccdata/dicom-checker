FROM flywheel/python:3.12-alpine 

RUN apk update && apk upgrade && apk --no-cache add build-base cmake gcc g++;

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

# Installing main dependencies
COPY requirements.txt $FLYWHEEL/
RUN pip install --no-cache-dir -r $FLYWHEEL/requirements.txt

# Installing the current project (most likely to change, above layer can be cached)
COPY ./ $FLYWHEEL/
RUN pip install --no-cache-dir .

# Configure entrypoint
RUN chmod a+x $FLYWHEEL/run.py
ENTRYPOINT ["python", "/flywheel/v0/run.py"]
