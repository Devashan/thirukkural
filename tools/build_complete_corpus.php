#!/usr/bin/env php
<?php

declare(strict_types=1);

$root = dirname(__DIR__);
$development = $root . '/datasets/development';
$version = '2026.10.28.1';
$sourceId = 'dikshitar-1949-project-madurai';
$sourceUrl = 'https://www.projectmadurai.org/pm_etexts/utf8/pmuni0665.html';
$sourceCredit = 'V. R. Ramachandra Dikshitar, Thirukkural English Translation (1949), Project Madurai electronic text';

$titles = [
    1 => 'In Praise of God', 'In Praise of Rain', 'On the Greatness of Renunciation',
    'On Dharma', 'On Family Life', 'On Wives', 'On Sons', 'Loving-Kindness',
    'On Hospitality', 'On Sweet Words', 'On Gratitude', 'On Equity',
    'On Self-Control', 'On Right Conduct', 'On Adultery', 'On Patience',
    'On Envy', 'On Non-Coveting', 'On Not Back-Biting', 'On Frivolity of Speech',
    'On Fear of Evil Deeds', 'On Decorum', 'On Liberality', 'On Renown',
    'On Compassion', 'On Abstaining from Meat', 'On Penance', 'On Improper Conduct',
    'On Non-Stealing', 'On Truth', 'On Not Getting Angry', 'On Not Doing Evil',
    'On Not Killing', 'On Instability', 'On Renunciation', 'On True Knowledge',
    'On the Destruction of Desire', 'On Fate', 'On Majesty', 'On Learning',
    'On Non-Learning', 'On Hearing', 'On Knowledge', 'On Restraining Faults',
    'On Association with Elders', 'On Avoiding Low Company',
    'On Action after Due Deliberation', "On Knowing the Enemy's Strength",
    'On Knowing the Time', 'On Knowing the Place', 'Engaging Servants After Test',
    'On Appointment According to Merit', "On Cherishing One's Kindred",
    'Against Forgetfulness', 'On Righteous Sceptre', 'On Unrighteous Rule',
    'On Tyranny', 'On Kindliness', 'On Spies', 'On Exertion', 'Against Sloth',
    'On Perseverance', 'On Courage', 'On Ministers', 'On Good Speech',
    'On Purity in Action', 'On Resoluteness', 'On the Means of Action',
    'On Embassy', 'On Co-operation with King', "On Reading One's Intentions",
    'On Knowing the Assembly', 'Not to be Afraid of Assembly', 'On the Kingdom',
    'On Fortress', 'On Acquisition of Wealth', 'On the Value of an Army',
    'On Courage of the Army', 'On Friendship', 'On True Friendship',
    'On Old Friendship', 'On Base Alliance', 'On False Alliance', 'On Stupidity',
    'On Ignorance', 'On Discord', 'On Enmity', "On Knowing the Enemy's Strength",
    'Internal Foes', 'Not Censuring the Great', "On Following Women's Advice",
    'On Public Women', 'On Avoiding Wine', 'On Gambling', 'On Medicine',
    'On Noble Lineage', 'On Honour', 'On Greatness', 'On Good Conduct',
    'On Courtesy', 'On Unprofitable Wealth', 'On Modesty',
    "On Exalting One's Family", 'On Agriculture', 'On Poverty', 'On Begging',
    'On Fear of Begging', 'On Meanness', "On Lover's Distraction",
    "Reading Love's Signs", "The Ecstasy of Love's Union", 'On His Lady',
    'On the Affirmation of Love', 'Speaking Out Unabashed',
    'Rumours of Secret Love', 'The Pangs of Separation',
    'The Cry of the Separated', 'On Eyes That Languish',
    "Grieving Over Love's Pallor", 'Feeling All Alone',
    'Recollecting the Pleasures of Love', 'Dreams of Love', 'Sunset and Sorrow',
    'Wasting Away', 'Soliloquy of the Lady Love', 'On the Loss of Modesty',
    'On the Distress of each Towards the Other', 'On Speaking on the Signs',
    'On Yearning After Union', 'On Speaking with the Mind',
    "On Lovers' Misunderstanding", "On Subtlety of Lovers' Misunderstanding",
    "On the Pleasures of Lovers' Misunderstanding",
];

$iyals = [
    ['iyal_id' => 1, 'paal_no' => 1, 'order_in_paal' => 1, 'first' => 1, 'last' => 4, 'name_ta' => 'பாயிரவியல்', 'name_en' => 'Preface'],
    ['iyal_id' => 2, 'paal_no' => 1, 'order_in_paal' => 2, 'first' => 5, 'last' => 24, 'name_ta' => 'இல்லறவியல்', 'name_en' => 'Domestic Virtue'],
    ['iyal_id' => 3, 'paal_no' => 1, 'order_in_paal' => 3, 'first' => 25, 'last' => 37, 'name_ta' => 'துறவறவியல்', 'name_en' => 'Renunciation'],
    ['iyal_id' => 4, 'paal_no' => 1, 'order_in_paal' => 4, 'first' => 38, 'last' => 38, 'name_ta' => 'ஊழியல்', 'name_en' => 'Fate'],
    ['iyal_id' => 5, 'paal_no' => 2, 'order_in_paal' => 1, 'first' => 39, 'last' => 63, 'name_ta' => 'அரசியல்', 'name_en' => 'The State'],
    ['iyal_id' => 6, 'paal_no' => 2, 'order_in_paal' => 2, 'first' => 64, 'last' => 73, 'name_ta' => 'அமைச்சியல்', 'name_en' => 'Ministers of State'],
    ['iyal_id' => 7, 'paal_no' => 2, 'order_in_paal' => 3, 'first' => 74, 'last' => 95, 'name_ta' => 'அங்கவியல்', 'name_en' => 'Limbs of the State'],
    ['iyal_id' => 8, 'paal_no' => 2, 'order_in_paal' => 4, 'first' => 96, 'last' => 108, 'name_ta' => 'ஒழிபியல்', 'name_en' => 'The Residue'],
    ['iyal_id' => 9, 'paal_no' => 3, 'order_in_paal' => 1, 'first' => 109, 'last' => 115, 'name_ta' => 'களவியல்', 'name_en' => 'The Secret Union'],
    ['iyal_id' => 10, 'paal_no' => 3, 'order_in_paal' => 2, 'first' => 116, 'last' => 133, 'name_ta' => 'கற்பியல்', 'name_en' => 'Wedded Love'],
];

$meaningDrafts = [
    37 => "There is no need to explain virtue's fruit: it can be seen in the difference between the palanquin bearer and its rider.",
    184 => "Though you may speak harshly to someone's face, do not speak behind their back without regard for the harm that follows.",
    223 => "Giving before a person must voice the misery 'I have nothing' is found only in one of noble lineage.",
    268 => 'All other living beings revere the one who has gained mastery over his own life through self-control.',
    329 => 'To those who discern baseness, people whose trade is killing appear as people engaged in a degrading trade.',
    354 => 'Even mastery of the five senses is fruitless to those who lack true understanding.',
    388 => 'A king who upholds justice and protects his people will be regarded by them as their lord.',
];

$batches = [
    '1-30' => 'ai-reviewed-1-30',
    '31-40' => 'ai-reviewed-31-40',
    '41-50' => 'ai-reviewed-41-50',
    '51-60' => 'ai-reviewed-51-60-20261027',
    '61-70' => 'ai-reviewed-61-70-20261027',
    '71-80' => 'ai-reviewed-71-80-20261027',
    '81-90' => 'ai-reviewed-81-90-20261027',
    '91-100' => 'ai-reviewed-91-100-20261027',
    '101-110' => 'ai-reviewed-101-110-20261027',
    '111-120' => 'ai-reviewed-111-120-20261027',
    '121-133' => 'ai-reviewed-121-133-20261027',
];

function iyalForChapter(int $chapterNo, array $iyals): array
{
    foreach ($iyals as $iyal) {
        if ($chapterNo >= $iyal['first'] && $chapterNo <= $iyal['last']) {
            unset($iyal['first'], $iyal['last']);
            return $iyal;
        }
    }
    throw new RuntimeException("No iyal for chapter {$chapterNo}");
}

if (count($titles) !== 133 || array_keys($titles) !== range(1, 133)) {
    throw new RuntimeException('English chapter title table must cover chapters 1-133 exactly.');
}

foreach ($batches as $range => $sourceName) {
    $sourceDir = $development . '/' . $sourceName;
    $targetName = 'ai-reviewed-' . $range . '-20261028';
    $targetDir = $development . '/' . $targetName;
    $chapterDir = $targetDir . '/chapters';
    if (!is_dir($chapterDir) && !mkdir($chapterDir, 0777, true) && !is_dir($chapterDir)) {
        throw new RuntimeException("Unable to create {$chapterDir}");
    }

    $manifest = json_decode((string) file_get_contents($sourceDir . '/manifest.json'), true, 512, JSON_THROW_ON_ERROR);
    $manifest['dataset_version'] = $version;
    $manifest['coverage']['ai_idiomatic_translation_drafts'] = $manifest['counts']['kurals'];
    $manifest['coverage']['idiomatic_candidates_withheld'] = 0;
    $manifest['structure'] = [
        'english_chapter_titles' => $manifest['counts']['chapters'],
        'iyal_count_in_full_corpus' => 10,
        'source_id' => $sourceId,
        'source_locator' => $sourceUrl,
        'source_credit' => $sourceCredit,
    ];
    $manifest['chapter_files'] = [];

    foreach (glob($sourceDir . '/chapters/chapter-*.json') as $sourcePath) {
        $document = json_decode((string) file_get_contents($sourcePath), true, 512, JSON_THROW_ON_ERROR);
        $document['dataset_version'] = $version;
        $chapterNo = (int) $document['chapter']['chapter_no'];
        $document['chapter']['name_en'] = $titles[$chapterNo];
        $document['chapter']['name_en_source_id'] = $sourceId;
        $document['chapter']['name_en_source_locator'] = $sourceUrl . '#contents';
        $document['chapter']['name_en_credit'] = $sourceCredit;
        $iyal = iyalForChapter($chapterNo, $iyals);
        $iyal['division_source_id'] = $sourceId;
        $iyal['division_source_locator'] = $sourceUrl . '#structure';
        $iyal['source_credit'] = $sourceCredit;
        $document['chapter']['iyal'] = $iyal;

        foreach ($document['kurals'] as &$kural) {
            $number = (int) $kural['kural_no'];
            if (!isset($meaningDrafts[$number])) {
                continue;
            }
            $kural['idiomatic_translation']['text'] = $meaningDrafts[$number];
            $locators = $kural['idiomatic_translation']['additional_source_locators'] ?? [];
            $locator = "https://thirukkural.io/kural/{$number}";
            if (!in_array($locator, $locators, true)) {
                $locators[] = $locator;
            }
            $kural['idiomatic_translation']['additional_source_locators'] = $locators;
        }
        unset($kural);

        $filename = basename($sourcePath);
        $targetPath = $chapterDir . '/' . $filename;
        $encoded = json_encode(
            $document,
            JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR
        ) . "\n";
        file_put_contents($targetPath, $encoded);
        $manifest['chapter_files']['chapters/' . $filename] = hash('sha256', $encoded);
    }

    ksort($manifest['chapter_files']);
    file_put_contents(
        $targetDir . '/manifest.json',
        json_encode($manifest, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR) . "\n"
    );
    file_put_contents(
        $targetDir . '/README.md',
        "# Complete reader metadata {$range}\n\n"
        . "Immutable development snapshot {$version}. It adds sourced English chapter headings and iyal boundaries to every chapter, and supplies commentary-backed AI-assisted drafts for any of Kurals 37, 184, 223, 268, 329, 354 and 388 in this range. Tamil text and review flags are unchanged. See `docs/reader-metadata-2026-10-28.md`.\n"
    );
}

fwrite(STDOUT, "Built {$version}: 133 sourced chapter titles, 10 sourced iyals and 7 completed draft meanings.\n");
