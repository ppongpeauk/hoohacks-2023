import Nav from "@/components/Nav";
import styles from "@/styles/Home.module.css";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import Head from "next/head";
import Link from "next/link";
import { useRef, useState } from "react";
import { TailSpin } from "react-loader-spinner";

interface FormData {
  target: {
    resumeFile: File;
  };
}

export function PillList({ list }: { list: string[] }) {
  return (
    <div className={styles.pillList}>
      {list.map((entry: string) => {
        return (
          <span className={styles.pill} key={entry}>
            {entry}{" "}
          </span>
        );
      })}
    </div>
  );
}

export default function Home() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileUploadRef = useRef<HTMLInputElement>(null);

  const [results, setResults] = useState<any>(null);
  const [selectedJob, setSelectedJob] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    setError(null);
    setResults(null);
    setSelectedJob(null);
    setLoading(true);
    // const exampleData = {
    //   resumeParsedData: {
    //     skills: ["html", "css"],
    //   },
    //   jobResults: [
    //     {
    //       title: "Software Engineer",
    //       company: "Google",
    //       location: "Mountain View, CA",
    //       matchedAttributes: {
    //         skills: ["html", "css"],
    //       },
    //       applicationLink: "https://google.com",
    //     }
    //   ]
    // };
    // setResults({
    //   resumeParsedData: {
    //     skills: ["html", "css"],
    //   },
    //   jobResults: [
    //     {
    //       title: "Software Engineer",
    //       company: "Google",
    //       location: "Mountain View, CA",
    //       matchedAttributes: {
    //         skills: ["html", "css"],
    //       },
    //       applicationLink: "https://google.com",
    //     },
    //   ],
    // });
    const fileInput = fileUploadRef.current;
    if (fileInput && fileInput.files && fileInput.files.length > 0) {
      const file = fileInput.files[0];
      const formData = new FormData();
      formData.append("file", file);
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/resume`, {
        method: "POST",
        body: formData,
      })
        .then((res) => res.json())
        .then((data) => {
          setResults(data);
          setLoading(false);
        })
        .catch((err) => {
          setError("There was a problem while processing your resume.");
          setLoading(false);
        });
    } else {
      setError("Please select a file to upload.");
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>ResuMatch</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Nav />
      <main className={styles.main}>
        <div className={styles.section}>
          <div className={styles.form}>
            <h2 className={styles.header}>Upload Resume</h2>
            {error ? (
              <div className={styles.error}>
                {error ? <p>{error}</p> : null}
              </div>
            ) : null}
            <form onSubmit={handleSubmit}>
              <input
                ref={fileUploadRef}
                className={styles.input}
                id="resumeFile"
                type="file"
                accept=".pdf"
                disabled={loading}
              ></input>
              <button className={styles.submitButton} disabled={loading}>
                {loading ? <TailSpin height="24" color="#000" /> : "Search"}
              </button>
            </form>
          </div>
          <div className={styles.resumePreview}>
            <h2 className={styles.header}>Data Gathered</h2>
            <br />
            {results ? (
              <>
                <h3>Skills</h3>
                <PillList list={results.resumeParsedData.skills} />
              </>
            ) : (
              <h3 className={styles.greyText}>Upload a Resume...</h3>
            )}
          </div>
        </div>
        <div className={styles.section}>
          <div className={styles.jobsList}>
            <h2 className={styles.header}>Matched Jobs</h2>
            <br />
            {results ? (
              results.jobResults.map((job: any) => {
                return (
                  <div className={styles.jobListing} key={job}>
                    <button
                      className={styles.jobListing__button}
                      onClick={() => {
                        setSelectedJob(job) as any;
                      }}
                    >
                      <div className={styles.jobListing__info}>
                        <h3>{job.title}</h3>
                        <p>{job.company}</p>
                        <p>{job.location}</p>
                      </div>
                    </button>
                  </div>
                );
              })
            ) : (
              <h3 className={styles.greyText}>Upload a Resume...</h3>
            )}
          </div>
        </div>
        <div className={styles.section}>
          <div className={styles.jobsList}>
            <h2 className={styles.header}>Job Details</h2>
            <br />
            {selectedJob ? (
              <>
                <h2>{selectedJob.title}</h2>
                <p>{selectedJob.company}</p>
                <p>{selectedJob.location}</p>
                <br />
                <h3>Matching Skills</h3>
                <PillList list={selectedJob.matchedAttributes.skills} />
                <br />
                <Link
                  className={styles.submitButton}
                  href={selectedJob.applicationLink}
                >
                  Apply
                </Link>
              </>
            ) : (
              <h3 className={styles.greyText}>Select a Job...</h3>
            )}
          </div>
        </div>
      </main>
    </>
  );
}
