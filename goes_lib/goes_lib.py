import boto3
import json
import pytz

from satellite_settings import satellite_settings


class GOES:
    def __init__(self, s3_key, s3_secret, timezone="GMT"):
        """Initializes class, starts S3 boto3 client."""
        self.s3 = boto3.client(
            "s3",
            use_ssl=False,
            verify=False,
            aws_access_key_id=s3_key,
            aws_secret_access_key=s3_secret,
        )
        # Loads dictionary of satellites & their settings
        self.satellite_dict = satellite_settings

    def get_s3_keys(self, bucket, prefix=""):
        """
        Generate the keys in an S3 bucket.

        :param bucket: Name of the S3 bucket.
        :param prefix: Only fetch keys that start with this prefix (optional).
        """
        kwargs = {"Bucket": bucket}

        if isinstance(prefix, str):
            kwargs["Prefix"] = prefix

        while True:
            resp = self.s3.list_objects_v2(**kwargs)
            if "Contents" in resp:
                for obj in resp["Contents"]:
                    key = obj["Key"]
                    if key.startswith(prefix):
                        yield key
            else:
                yield None

            try:
                kwargs["ContinuationToken"] = resp["NextContinuationToken"]
            except KeyError:
                break

    def gen_s3_prefix(self, product, band, imager_name, requested_datetime):
        # Returns S3 folder path for provided values
        return f"{product}/{requested_datetime.year}/{str(requested_datetime.timetuple().tm_yday).zfill(3)}/{str(requested_datetime.hour).zfill(2)}/OR_{product}-{imager_name}{str(band).zfill(2)}"

    def save_s3_file(self, bucket, s3_key, file_name, download_loc=""):
        self.s3.download_file(bucket, s3_key, f"{download_loc}{file_name}.nc")

    def get_keys_by_datetime(
        self,
        band,
        requested_datetime,
        satellite,
        requested_timezone=pytz.timezone("GMT"),
    ):
        local_dt = requested_timezone.localize(requested_datetime, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)

        return self.get_s3_keys(
            satellite["aws_sat_name"],
            prefix=self.gen_s3_prefix(
                satellite["aws_product_name"], band, satellite["imager_name"], utc_dt
            ),
        )
