"""
Schedule running the Internet Archive upload Add-On on a project of documents on a schedule.
"""
from itertools import islice
from documentcloud.addon import AddOn


class Scheduler(AddOn):
    """Schedules the IA upload Add-On over a search query in batches."""

    def main(self):
        """Runs the IA upload Add-On on a batch of documents."""
        self.client.session.headers.update({'User-Agent': 'IA Upload Scheduler Add-On'})
        batch_size = self.data.get("batch_size")
        query = self.query
        batch_num = 1

        run_id = 175  # Internet Archive upload Add-On

        # make sure already-uploaded docs are excluded, without duplicating the clause
        if "data_ia_url" not in query:
            query = f"{query} -data_ia_url:*".strip()

        print(query)

        documents = self.client.documents.search(query)

        for i in range(batch_num):
            # Pull out the IDs for a batch of the documents
            doc_ids = [
                d.id for d in islice(documents, i * batch_size, (i + 1) * batch_size)
            ]
            print(doc_ids)
            self.client.post(
                "addon_runs/",
                json={
                    "addon": run_id,
                    "parameters": {},
                    "documents": doc_ids,
                    "dismissed": True,
                },
            )

if __name__ == "__main__":
    Scheduler().main()
