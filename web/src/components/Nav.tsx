import Link from "next/link";
import styles from "./Nav.module.css";

export default function Nav() {
  return (
    <nav className={styles.nav}>
      <div>
        <Link href="/">
          <img src="/logo.png" alt="LinkedOut" width={128} />
        </Link>
      </div>
    </nav>
  );
}