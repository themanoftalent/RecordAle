cask "recordale" do
  arch arm: "arm64", intel: "x64"

  version "1.4.0"

  url "https://github.com/themanoftalent/RecordAle/releases/download/v#{version}/RecordAle-#{arch}.dmg"
  name "RecordAle"
  desc "Creator-focused screen recorder and video editor with auto-zoom, cursor effects, and more"
  homepage "https://github.com/themanoftalent/RecordAle"

  livecheck do
    url :url
    strategy :github_latest
  end

  app "RecordAle.app"

  zap trash: [
    "~/Library/Application Support/RecordAle",
    "~/Library/Application Support/RecoreAle",
    "~/Library/Application Support/Recordly",
    "~/Library/Preferences/com.softai.recordale.plist",
    "~/Library/Saved Application State/com.softai.recordale.savedState",
  ]
end
