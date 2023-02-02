IMAGE_TAG=$1
# docker run --rm anchore/grype:latest redis:5.0-alpine3.10 -o json > a.json
image_tag=
docker run --rm anchore/grype:latest $IMAGE_TAG -o json > $image_tag.json

