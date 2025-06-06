import argparse
import statistics
import time
import requests


def benchmark(url: str, image_path: str, model: str, runs: int) -> float:
    times = []
    for i in range(runs):
        with open(image_path, "rb") as img_file:
            files = {"image": (image_path, img_file, "image/jpeg")}
            data = {"model": model}
            start = time.perf_counter()
            try:
                response = requests.post(url, files=files, data=data)
            except Exception as exc:
                print(f"Request {i + 1} failed: {exc}")
                continue
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            print(f"Request {i + 1}: status {response.status_code} - {elapsed:.3f}s")
    if not times:
        raise RuntimeError("No requests completed successfully")
    avg = statistics.mean(times)
    print(f"Average response time over {len(times)} runs: {avg:.3f}s")
    return avg


def main():
    parser = argparse.ArgumentParser(description="Benchmark inference server")
    parser.add_argument("--url", default="http://localhost:8001/predict/", help="Prediction endpoint URL")
    parser.add_argument("--image", default="imagenesPrueba/prueba.jpg", help="Path to image for testing")
    parser.add_argument("--model", default="fake", help="Model name to send")
    parser.add_argument("--runs", type=int, default=20, help="Number of requests to send")
    args = parser.parse_args()
    benchmark(args.url, args.image, args.model, args.runs)


if __name__ == "__main__":
    main()

