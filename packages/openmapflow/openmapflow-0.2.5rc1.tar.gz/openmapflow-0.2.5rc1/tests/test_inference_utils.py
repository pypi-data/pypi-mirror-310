from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from openmapflow.bbox import BBox

try:
    from openmapflow.inference_utils import (
        find_missing_predictions,
        gdal_cmd,
        get_available_bboxes,
        get_available_models,
        get_gcs_file_amount,
        get_gcs_file_dict_and_amount,
        get_status,
        make_new_predictions,
    )

    SKIP_TEST = False
except ImportError:
    SKIP_TEST = True


class MockBlob:
    def __init__(self, name):
        self.name = name


class TestInferenceUtils(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake_bucket = "fake_bucket"
        cls.namibia_bbox_name = (
            "Namibia_North_2020_min_lat=-19.4837_min_lon=14.1513_max_lat=-17.3794_"
            + "max_lon=25.0448_dates=2020-09-01_2021-09-01_all_final/"
        )
        cls.namibia_expected_bbox = BBox(
            -19.4837,
            -17.3794,
            14.1513,
            25.0448,
            name=f"gs://{cls.fake_bucket}/{cls.namibia_bbox_name}",
        )

    def setUp(self) -> None:
        if SKIP_TEST:
            self.skipTest("google-cloud-storage is not installed")

    @patch("openmapflow.inference_utils.requests")
    def test_get_available_models_200(self, mock_requests):
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.json.return_value = {
            "models": [
                {"modelName": "model1", "modelUrl": "model1.mar"},
                {"modelName": "model2", "modelUrl": "model2.mar"},
                {"modelName": "model3", "modelUrl": "model3.mar"},
            ]
        }
        models = get_available_models("https://fake-url.com/models")
        self.assertEqual(models, ["model1", "model2", "model3"])

    @patch("openmapflow.inference_utils.requests")
    def test_get_available_models_403(self, mock_requests):
        mock_requests.get.return_value.status_code = 403
        models = get_available_models("https://fake-url.com/models")
        self.assertEqual(models, [])

    @patch("openmapflow.inference_utils.storage")
    def test_get_available_bboxes_none(self, mock_storage):
        mock_storage_client = mock_storage.Client()
        mock_storage_client.list_blobs.return_value = []
        bboxes = get_available_bboxes(buckets_to_check=["fake_bucket"])
        self.assertEqual(bboxes, [])
        mock_storage_client.list_blobs.assert_called_once()

    @patch("openmapflow.inference_utils.storage")
    def test_get_available_bboxes_no_bucket(self, mock_storage):
        self.assertRaises(ValueError, get_available_bboxes, [])

    @patch("openmapflow.inference_utils.storage")
    def test_get_available_bboxes(self, mock_storage):
        mock_storage_client = mock_storage.Client()
        mock_storage_client.list_blobs.return_value = [MockBlob(self.namibia_bbox_name)]
        actual_bbox = get_available_bboxes(buckets_to_check=[self.fake_bucket])[0]
        self.assertEqual(actual_bbox, self.namibia_expected_bbox)

    @patch("openmapflow.inference_utils.storage")
    def test_get_available_bboxes_avoid_dupes(self, mock_storage):
        mock_storage_client = mock_storage.Client()
        mock_storage_client.list_blobs.return_value = [
            MockBlob(self.namibia_bbox_name)
        ] * 20
        bboxes = get_available_bboxes(buckets_to_check=[self.fake_bucket])
        self.assertEqual(len(bboxes), 1)

    @patch("openmapflow.inference_utils.storage")
    def test_get_available_bboxes_integers(self, mock_storage):
        namibia_bbox_name_ints = (
            "Namibia_North_2020_min_lat=-19_min_lon=14_max_lat=-17_"
            + "max_lon=25_dates=2020-09-01_2021-09-01_all_final/"
        )
        namibia_expected_bbox = BBox(
            -19, -17, 14, 25, name=f"gs://{self.fake_bucket}/{namibia_bbox_name_ints}"
        )
        mock_storage_client = mock_storage.Client()
        mock_storage_client.list_blobs.return_value = [MockBlob(namibia_bbox_name_ints)]
        actual_bbox = get_available_bboxes(buckets_to_check=[self.fake_bucket])[0]
        self.assertEqual(actual_bbox, namibia_expected_bbox)

    @patch("openmapflow.inference_utils.storage")
    def test_get_gcs_file_amount(self, mock_storage):
        mock_storage_client = mock_storage.Client()
        mock_storage_client.list_blobs.return_value = []
        self.assertEqual(get_gcs_file_amount("fake_bucket", "fake_prefix"), 0)
        mock_storage_client.list_blobs.return_value = [MockBlob("file")]
        self.assertEqual(get_gcs_file_amount("fake_bucket", "fake_prefix"), 1)
        mock_storage_client.list_blobs.return_value = [MockBlob("file")] * 100
        self.assertEqual(get_gcs_file_amount("fake_bucket", "fake_prefix"), 100)

    @patch("openmapflow.inference_utils.storage")
    def test_get_gcs_file_dict_and_amount(self, mock_storage):
        mock_storage_client = mock_storage.Client()
        mock_storage_client.list_blobs.return_value = [
            MockBlob("parent1/file1"),
            MockBlob("parent1/file2"),
            MockBlob("parent1/file3"),
            MockBlob("parent2/file4"),
            MockBlob("parent2/file5"),
            MockBlob("parent2/file6"),
        ]
        actual_files_dict, actual_amount = get_gcs_file_dict_and_amount(
            "fake_bucket", "fake_prefix"
        )
        self.assertEqual(actual_amount, 6)
        self.assertEqual(actual_files_dict["parent1"], ["file1", "file2", "file3"])
        self.assertEqual(actual_files_dict["parent2"], ["file4", "file5", "file6"])

    @patch("openmapflow.inference_utils.storage")
    def test_get_gcs_file_dict_and_amount_nested(self, mock_storage):
        mock_storage_client = mock_storage.Client()
        mock_storage_client.list_blobs.return_value = [
            MockBlob("grandparent1/parent1/file1"),
            MockBlob("grandparent1/parent1/file2"),
            MockBlob("grandparent1/parent1/file3"),
            MockBlob("grandparent1/parent2/file4"),
            MockBlob("grandparent1/parent2/file5"),
            MockBlob("grandparent2/parent2/file6"),
        ]
        actual_files_dict, actual_amount = get_gcs_file_dict_and_amount(
            "fake_bucket", "fake_prefix"
        )
        self.assertEqual(actual_amount, 6)
        self.assertEqual(
            actual_files_dict[str(Path("grandparent1/parent1"))],
            ["file1", "file2", "file3"],
        )
        self.assertEqual(
            actual_files_dict[str(Path("grandparent1/parent2"))], ["file4", "file5"]
        )
        self.assertEqual(
            actual_files_dict[str(Path("grandparent2/parent2"))], ["file6"]
        )

    @patch("openmapflow.inference_utils.storage")
    def test_get_gcs_file_dict_and_amount_pred_sub(self, mock_storage):
        mock_storage_client = mock_storage.Client()
        mock_storage_client.list_blobs.return_value = [MockBlob("parent1/pred_file1")]
        actual_files_dict, actual_amount = get_gcs_file_dict_and_amount(
            "fake_bucket", "fake_prefix"
        )
        self.assertEqual(actual_amount, 1)
        self.assertEqual(actual_files_dict["parent1"], ["file1"])

    @patch("openmapflow.ee_exporter.ee")
    @patch("openmapflow.inference_utils.storage")
    def test_get_status(self, mock_storage, mock_ee):
        mock_storage_client = mock_storage.Client()
        mock_storage_client.list_blobs.return_value = [MockBlob("file")] * 100
        mock_ee.data.getTaskList.return_value = [
            {"state": "READY", "description": "fake_prefix"}
        ] * 10
        self.assertEqual(get_status("fake_prefix"), (10, 100, 100))

    @patch("openmapflow.ee_exporter.ee")
    @patch("openmapflow.inference_utils.storage")
    def test_get_status_special_chars(self, mock_storage, mock_ee):
        mock_storage_client = mock_storage.Client()
        mock_storage_client.list_blobs.return_value = [MockBlob("file")] * 100
        mock_ee.data.getTaskList.return_value = [
            {"state": "READY", "description": "fake_prefix_lon-10"}
        ] * 10
        self.assertEqual(get_status("fake_prefix_lon=10"), (10, 100, 100))

    @patch("openmapflow.ee_exporter.ee")
    @patch("openmapflow.inference_utils.storage")
    def test_get_status_prefix(self, mock_storage, mock_ee):
        mock_storage_client = mock_storage.Client()
        mock_storage_client.list_blobs.return_value = [MockBlob("file")] * 100
        mock_ee.data.getTaskList.return_value = [
            {"state": "READY", "description": "fake_prefix_lon_10"}
        ] * 10
        self.assertEqual(get_status("fake_prefix"), (10, 100, 100))

    @patch("openmapflow.inference_utils.storage")
    def test_find_missing_predictions(self, mock_storage):
        mock_storage_client = mock_storage.Client()
        data_available = [
            MockBlob("parent1/file1"),
            MockBlob("parent1/file2"),
            MockBlob("parent1/file3"),
            MockBlob("parent2/file4"),
            MockBlob("parent2/file5"),
            MockBlob("parent2/file6"),
        ]
        preds_made = data_available[:4]

        def full_and_missing_return():
            yield data_available
            yield preds_made

        mock_storage_client.list_blobs.side_effect = full_and_missing_return()

        actual_missing_preds = find_missing_predictions("fake_prefix")
        self.assertListEqual(
            sorted(actual_missing_preds["parent2"]), ["file5", "file6"]
        )

    @patch("openmapflow.inference_utils.storage")
    def test_find_missing_predictions_none(self, mock_storage):
        mock_storage_client = mock_storage.Client()
        data_available = [
            MockBlob("parent1/file1"),
            MockBlob("parent1/file2"),
            MockBlob("parent1/file3"),
            MockBlob("parent2/file4"),
            MockBlob("parent2/file5"),
            MockBlob("parent2/file6"),
        ]
        preds_made = data_available

        def full_and_missing_return():
            yield data_available
            yield preds_made

        mock_storage_client.list_blobs.side_effect = full_and_missing_return()

        actual_missing_preds = find_missing_predictions("fake_prefix")
        self.assertEqual(actual_missing_preds, {})

    @patch("openmapflow.inference_utils.storage")
    def test_find_missing_predictions_all(self, mock_storage):
        mock_storage_client = mock_storage.Client()
        data_available = [
            MockBlob("parent1/file1"),
            MockBlob("parent1/file2"),
            MockBlob("parent1/file3"),
            MockBlob("parent2/file4"),
            MockBlob("parent2/file5"),
            MockBlob("parent2/file6"),
        ]
        preds_made = []

        def full_and_missing_return():
            yield data_available
            yield preds_made

        mock_storage_client.list_blobs.side_effect = full_and_missing_return()

        actual_missing_preds = find_missing_predictions("fake_prefix")
        self.assertEqual(actual_missing_preds["parent1"], ["file1", "file2", "file3"])
        self.assertEqual(actual_missing_preds["parent2"], ["file4", "file5", "file6"])

    @patch("openmapflow.inference_utils.storage")
    def test_make_new_predictions(self, mock_storage):
        make_new_predictions(
            missing={"parent1": ["file1", "file2", "file3"]}, bucket_name="fake_bucket"
        )
        mock_storage.Client.assert_called()
        mock_storage_client = mock_storage.Client()
        mock_storage_client.bucket.assert_called_once()
        mock_storage_bucket = mock_storage_client.bucket("fake_bucket")
        blob_call_args = [
            call[0][0] for call in mock_storage_bucket.blob.call_args_list
        ]
        rename_call_args = [
            call[0][1] for call in mock_storage_bucket.rename_blob.call_args_list
        ]
        for i in [1, 2, 3]:
            original_tif = f"parent1/file{i}.tif"
            retry_tif = f"parent1/file{i}-retry.tif"
            self.assertIn(original_tif, blob_call_args)
            self.assertIn(retry_tif, rename_call_args)

    @patch("openmapflow.inference_utils.os.system")
    def test_gdal_cmd_buildvrt(self, mock_system):
        gdal_cmd(
            cmd_type="gdalbuildvrt", out_file="fake_file.vrt", in_file="fake_files/*"
        )
        mock_system.assert_called_once()
        mock_system.assert_called_with("gdalbuildvrt fake_file.vrt fake_files/*")

    @patch("openmapflow.inference_utils.os.system")
    def test_gdal_cmd_translate(self, mock_system):
        gdal_cmd(
            cmd_type="gdal_translate", out_file="fake_file.tif", in_file="fake_file.vrt"
        )
        mock_system.assert_called_once()
        mock_system.assert_called_with(
            "gdal_translate -a_srs EPSG:4326 -of GTiff fake_file.vrt fake_file.tif"
        )
