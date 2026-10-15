cask "recoreale" do
  arch arm: "arm64", intel: "x64"

  version "1.1.14"

  url "https://github.com/themanoftalent/RecoreAle/releases/download/v#{version}/RecoreAle-#{arch}.dmg"
  name "RecoreAle"
  desc "Creator-focused screen recorder and video editor with auto-zoom, cursor effects, and more"
  homepage "https://github.com/themanoftalent/RecoreAle"

  livecheck do
    url :url
    strategy :github_latest
  end

  app "RecoreAle.app"

  zap trash: [
    "~/Library/Application Support/RecoreAle",
    "~/Library/Application Support/Recordly",
    "~/Library/Preferences/com.softai.recoreale.plist",
    "~/Library/Saved Application State/com.softai.recoreale.savedState",
  ]
end
