terraform {
  backend "s3" {
    bucket = "movies-statefile"
    key    = "tfstate"
    region = "eu-north-1"
  }
}